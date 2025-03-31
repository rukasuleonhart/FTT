import pytest
from http import HTTPStatus
from fastapi.testclient import TestClient
from jwt import decode

from ftt.schemas import UserPublic
from ftt.app import app
from ftt.database import get_session
from ftt.security import ALGORITHM, SECRET_KEY, create_access_token


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as test_client:
        app.dependency_overrides[get_session] = get_session_override
        yield test_client
        del app.dependency_overrides[get_session]


@pytest.fixture()
def user():
    return {
        "id": 1,
        "username": "Teste",
        "password": "123456",
        "email": "teste@test.com",
    }


@pytest.fixture()
def token(user):
    return create_access_token({"sub": user["email"]})


def test_pagina_inicial(client: TestClient):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá, seja bem vindo !"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "rukasuleonhart",
            "password": "ruka102030",
            "email": "rukasuleonhart@gmail.com",
        },
    )
    
    assert response.status_code == HTTPStatus.CREATED
    user_data = response.json()
    assert "id" in user_data
    assert user_data["username"] == "rukasuleonhart"
    assert user_data["email"] == "rukasuleonhart@gmail.com"


def test_read_users(client, token, user):
    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [
        {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
        }
    ]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user["id"]}',
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@test.com",
            "password": "mynewpassword",
            "id": user["id"],
        }
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@test.com",
        "id": user["id"],
    }