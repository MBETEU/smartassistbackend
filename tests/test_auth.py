import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.core.config import settings

# ✅ Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Crée les tables pour les tests
Base.metadata.create_all(bind=engine)

# Override la dépendance get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def test_user():
    """Crée un utilisateur avant le test"""
    user_data = {"email": "test@example.com", "password": "123456"}
    client.post("/api/auth/register", json=user_data)
    return user_data


def test_login_success(test_user):
    """✅ Teste un login réussi"""
    response = client.post("/api/auth/login", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_failure():
    """❌ Teste un login avec mauvais mot de passe"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Identifiants invalides."
