import os, tempfile
_fd, _path = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = "sqlite:///" + _path
os.environ["SECRET_KEY"] = "test-secret-key-for-flowforge-tests-not-production"
os.environ["APP_ENV"] = "test"
os.environ["CORS_ORIGINS"] = "http://localhost:5173"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
