from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import settings
from .database import Base, engine, get_db
from .models import User, Workflow, WorkflowRun
from .schemas import RegisterIn, LoginIn, WorkflowCreate, WorkflowUpdate, RunCreate
from .security import hash_password, verify_password, create_access_token, get_current_user, require_admin
from .workflow_engine import validate_definition, execute_workflow, WorkflowValidationError

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit_api])
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="FlowForge AI API", version="1.0.0", debug=settings.debug, lifespan=lifespan, docs_url="/docs" if settings.app_env != "production" else None, redoc_url=None)
@app.get("/")
def root():
    return {
        "message": "Welcome to FlowForge AI API",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=False, allow_methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"], allow_headers=["Authorization","Content-Type"], max_age=600)
if settings.app_env.lower() == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts
    )

@app.middleware("http")
async def secure_headers_and_body_limit(request: Request, call_next):
    length = request.headers.get("content-length")
    if length:
        try:
            if int(length) > settings.max_request_bytes:
                return JSONResponse(status_code=413, content={"detail":"Request body too large"})
        except ValueError:
            return JSONResponse(status_code=400, content={"detail":"Invalid Content-Length"})
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if request.url.path not in {
        "/docs",
        "/openapi.json",
        "/docs/oauth2-redirect",
    }:
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
        )
    response.headers["Cache-Control"] = "no-store"
    if settings.app_env == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/api/auth/register", status_code=201)
@limiter.limit(settings.rate_limit_auth)
def register(request: Request, payload: RegisterIn, db: Session = Depends(get_db)):
    email = str(payload.email).lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(email=email, password_hash=hash_password(payload.password), role="user")
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token":create_access_token(user),"token_type":"bearer","user":{"id":user.id,"email":user.email,"role":user.role}}

@app.post("/api/auth/login")
@limiter.limit(settings.rate_limit_auth)
def login(request: Request, payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if not user or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token":create_access_token(user),"token_type":"bearer","user":{"id":user.id,"email":user.email,"role":user.role}}

@app.get("/api/me")
def me(user: User = Depends(get_current_user)):
    return {"id":user.id,"email":user.email,"role":user.role}

@app.get("/api/admin/overview")
def admin_overview(user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return {"message":"Admin access granted","users":db.query(User).count(),"workflows":db.query(Workflow).count(),"runs":db.query(WorkflowRun).count()}

@app.get("/api/workflows")
def list_workflows(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = db.scalars(select(Workflow).where(Workflow.owner_id == user.id).order_by(Workflow.updated_at.desc())).all()
    return [{"id":w.id,"name":w.name,"description":w.description,"definition":w.definition,"created_at":w.created_at,"updated_at":w.updated_at} for w in rows]

@app.post("/api/workflows", status_code=201)
def create_workflow(payload: WorkflowCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try: definition = validate_definition(payload.definition.model_dump())
    except WorkflowValidationError as exc: raise HTTPException(status_code=422, detail=str(exc))
    name = payload.name.strip()
    if not name: raise HTTPException(status_code=422, detail="Workflow name cannot be blank")
    workflow = Workflow(owner_id=user.id, name=name, description=payload.description.strip(), definition=definition)
    db.add(workflow); db.commit(); db.refresh(workflow)
    return {"id":workflow.id,"name":workflow.name,"description":workflow.description,"definition":workflow.definition,"created_at":workflow.created_at,"updated_at":workflow.updated_at}

@app.get("/api/workflows/{workflow_id}")
def get_workflow(workflow_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.scalar(select(Workflow).where(Workflow.id == workflow_id, Workflow.owner_id == user.id))
    if not w: raise HTTPException(status_code=404, detail="Workflow not found")
    return {"id":w.id,"name":w.name,"description":w.description,"definition":w.definition,"created_at":w.created_at,"updated_at":w.updated_at}

@app.patch("/api/workflows/{workflow_id}")
def update_workflow(workflow_id: int, payload: WorkflowUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.scalar(select(Workflow).where(Workflow.id == workflow_id, Workflow.owner_id == user.id))
    if not w: raise HTTPException(status_code=404, detail="Workflow not found")
    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        name = (data["name"] or "").strip()
        if not name: raise HTTPException(status_code=422, detail="Workflow name cannot be blank")
        w.name = name
    if data.get("description") is not None: w.description = data["description"].strip()
    if data.get("definition") is not None:
        try: w.definition = validate_definition(data["definition"])
        except WorkflowValidationError as exc: raise HTTPException(status_code=422, detail=str(exc))
    w.updated_at = datetime.now(timezone.utc)
    db.commit(); db.refresh(w)
    return {"id":w.id,"name":w.name,"description":w.description,"definition":w.definition,"created_at":w.created_at,"updated_at":w.updated_at}

@app.delete("/api/workflows/{workflow_id}", status_code=204)
def delete_workflow(workflow_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.scalar(select(Workflow).where(Workflow.id == workflow_id, Workflow.owner_id == user.id))
    if not w: raise HTTPException(status_code=404, detail="Workflow not found")
    db.delete(w); db.commit()

@app.post("/api/workflows/{workflow_id}/runs", status_code=201)
@limiter.limit("20/minute")
def run_workflow(request: Request, workflow_id: int, payload: RunCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.scalar(select(Workflow).where(Workflow.id == workflow_id, Workflow.owner_id == user.id))
    if not w: raise HTTPException(status_code=404, detail="Workflow not found")
    try:
        result, steps = execute_workflow(w.definition, payload.input_data)
        run = WorkflowRun(workflow_id=w.id, status="completed", input_data=payload.input_data, result_data=result, steps=steps, finished_at=datetime.now(timezone.utc))
    except WorkflowValidationError as exc:
        run = WorkflowRun(workflow_id=w.id, status="failed", input_data=payload.input_data, result_data={}, steps=[], error_message=str(exc), finished_at=datetime.now(timezone.utc))
    db.add(run); db.commit(); db.refresh(run)
    return {"id":run.id,"workflow_id":w.id,"status":run.status,"input_data":run.input_data,"result_data":run.result_data,"steps":run.steps,"error_message":run.error_message,"started_at":run.started_at,"finished_at":run.finished_at}

@app.get("/api/workflows/{workflow_id}/runs")
def list_runs(workflow_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = db.scalar(select(Workflow).where(Workflow.id == workflow_id, Workflow.owner_id == user.id))
    if not w: raise HTTPException(status_code=404, detail="Workflow not found")
    runs = db.scalars(select(WorkflowRun).where(WorkflowRun.workflow_id == w.id).order_by(WorkflowRun.started_at.desc()).limit(50)).all()
    return [{"id":r.id,"status":r.status,"input_data":r.input_data,"result_data":r.result_data,"steps":r.steps,"error_message":r.error_message,"started_at":r.started_at,"finished_at":r.finished_at} for r in runs]
