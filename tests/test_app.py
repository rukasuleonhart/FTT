import pytest
from http import HTTPStatus
from fastapi.testclient import TestClient
from ftt.schemas import UserPublic
from ftt.app import app
from ftt.database import get_session


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as test_client:
        app.dependency_overrides[get_session] = get_session_override
        yield test_client
        del app.dependency_overrides[get_session]


def test_pagina_inicial(client: TestClient):
    response = client.get("/")  # Act (agir)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {"message": "Olá, seja bem vindo !"}  # Assert (afirmar)


def test_create_user(client):
    response = client.post(  # Act (agir)
        "/users/",
        json={
            "username": "rukasuleonhart",
            "password": "ruka102030",
            "email": "rukasuleonhart@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED  # Assert (afirmar)
    user_data = response.json()
    assert "id" in user_data  # O id gerado automaticamente pelo banco de dados
    assert user_data["username"] == "rukasuleonhart"
    assert user_data["email"] == "rukasuleonhart@gmail.com"
    return user_data["id"]  # Retorna o ID criado para uso posterior


def test_read_users(client):
    response = client.get("/users/")  # Act (agir)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {"users": []}  # Assert (afirmar)


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")  # Act (agir)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {"users": [user_schema]}  # Assert (afirmar)


def test_update_user(client):
    # Criação do usuário antes de tentar a atualização
    user_id = test_create_user(client)
    
    # Agora tentamos a atualização usando o ID retornado
    response = client.put(  # Act (agir)
        f'/users/{user_id}',  # Usa o ID criado dinamicamente
        json={
            "id": user_id,
            "username": "rukasuleonhart2",
            "password": "ruka102030",
            "email": "rukasuleonhart2@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {  # Assert (afirmar)
            "id": user_id,
            "username": "rukasuleonhart2",
            "email": "rukasuleonhart2@gmail.com",
        }
