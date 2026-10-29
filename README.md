# FlowForge AI — Workflow Studio

A portfolio-grade AI workflow automation starter with a distinctive warm-paper / charcoal / coral interface, FastAPI backend, React + TypeScript frontend, workflow graph validation, execution history, and account-scoped data.

## Features
- Email/password registration and login; passwords hashed with Argon2.
- Expiring signed bearer tokens; admin route protected by a server-side role dependency.
- User-scoped workflow CRUD and execution history.
- DAG validation rejects duplicate IDs, invalid edges, self-edges, cycles, and oversized graphs.
- Workflow node types: trigger, transform, condition, demo AI summary, approval placeholder, disabled HTTP request, output.
- API rate limits, CORS allowlist, security headers, body-size guard, typed input validation.
- PostgreSQL via Docker Compose; SQLite for local quick-start.
- Tests and GitHub Actions CI.

## Important security notes
This is a security-conscious starter, **not a guarantee of being unhackable or a completed penetration test**. The generated archive has not been run against live dependency registries or an external scanner. After installing dependencies, run the audit commands below and fix current advisories before deployment.

Known limitations: no email verification, password reset, MFA, refresh-token revocation, durable job queue, or external AI integration. The AI summary node is deterministic demo behavior and does not call an LLM. HTTP request nodes are intentionally disabled to avoid SSRF. The browser stores a short-lived bearer token in localStorage; for higher-assurance production use an HttpOnly same-site cookie/BFF design plus CSRF protections. Database tables are created automatically for the MVP; use Alembic migrations for production.

## Quick start (local)
Requirements: Python 3.11+, Node.js 20+.

### Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
```
Generate a secret using `python -c "import secrets; print(secrets.token_urlsafe(48))"` and replace `SECRET_KEY` in `backend/.env`. Then:
```bash
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```
Open `http://localhost:5173`. API defaults to `http://localhost:8000`.

### Docker
At project root:
```bash
cp backend/.env.example backend/.env
# Change SECRET_KEY before running.
docker compose up --build
```
Open `http://localhost:5173`.

## Checks
```bash
cd backend && pytest -q
pip-audit -r requirements.txt
cd ../frontend && npm install && npm audit && npm run build
```
Audit results depend on the package registry at the time you run them. No live audit is claimed by this archive.

## Production checklist
- Use HTTPS, exact CORS origins, a strong unique secret, and `DEBUG=false`.
- Use managed PostgreSQL with TLS, backups, and a least-privilege database account.
- Configure reverse proxy / trusted client IP handling before relying on IP-based rate limiting.
- Add email verification, password reset, MFA if appropriate, monitoring, backups, and migrations.
- Keep arbitrary outbound HTTP and code execution disabled unless SSRF/sandboxing controls are designed and tested.
- Never put private provider keys in `VITE_*` variables; those are exposed to browsers.
