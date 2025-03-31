import pytest
from fastapi.testclient import TestClient
from ftt.app import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ftt.models import table_registry, User


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

@pytest.fixture()
def user(session):
    user = User(username='Teste', email='teste@test.com', password='123456')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user