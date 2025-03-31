import pytest
from fastapi.testclient import TestClient
from http import HTTPStatus
from ftt.app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ftt.models import table_registry, User
from ftt.database import get_session


@pytest.fixture()
def client(session):
    def get_session_override():
        return session
    
    with TestClient(app) as test_client:
        app.dependency_overrides[get_session] = get_session_override
        yield test_client
        app.dependency_overrides.clear()

@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:', 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with SessionLocal() as session:
        yield session
    table_registry.metadata.drop_all(engine)

from ftt.security import get_password_hash

@pytest.fixture()
def user(session):
    user = User(username='Teste', email='teste@test.com', password='123456')

    session.add(user)
    session.commit()
    session.refresh(user)

    print("Usuário criado:", user.__dict__)  # Verifique se o usuário foi persistido corretamente
    return user



@pytest.fixture()
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.password},
    )
    print("Resposta do /token:", response.status_code, response.json())  # Debug
    return response.json().get('access_token')  # Use .get() para evitar erro caso a chave não exista


