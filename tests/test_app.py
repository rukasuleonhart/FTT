from http import HTTPStatus
from fastapi.testclient import TestClient
from ftt.app import app

def test_pagina_inicial(client: TestClient):
    response = client.get("/")  # Act (agir)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {"message": "Olá, seja bem vindo !"}  # Assert (afirmar)

def test_create_user(client: TestClient):
    response = client.post(  # Act (agir)
        "/users/",
        json={
            "username": "rukasuleonhart",
            "password": "ruka102030",
            "email": "rukasuleonhart@gmail.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED  # Assert (afirmar)
    assert response.json() == {  # Assert (afirmar)
        "username": "rukasuleonhart",
        "id": 1,
        "email": "rukasuleonhart@gmail.com",
    }
def test_read_users(client: TestClient):
    response = client.get("/users/")  # Act (agir)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {"users": [
        {
            "id": 1,
            "username": "rukasuleonhart",
            "email": "rukasuleonhart@gmail.com",
        }
    ]}  # Assert (afirmar)
    
def test_update_user(client: TestClient):
    response = client.put(  # Act (agir
        '/users/1',
        json={
            "id": 1,
            "username": "rukasuleonhart2",
            "password": "ruka102030",
            "email": "rukasuleonhart2@gmail.com",
        },
    )
    assert response.json() == {  # Assert (afirmar) 
            "id": 1,
            "username": "rukasuleonhart2",
            "email": "rukasuleonhart2@gmail.com",
        }
    