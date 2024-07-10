from fastapi.testclient import TestClient
from app.api import users
from app.sql_db import crud
import pytest


def test_create_user_first(unauth_client, test_user, db):
    users = crud.get_users(db)
    for user in users:
        print(user.id, user.email)
    response = unauth_client.post(
        "/users/", json={"email": test_user.email, "password": test_user.password}
    )
    users = crud.get_users(db)

    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
    assert response.json() == {
        "id": 1,
        "email": test_user.email,
        "is_active": True,
        "is_admin": None,
    }


def test_create_user_additional(unauth_client, users, test_user, db):
    users = crud.get_users(db)
    for user in users:
        print(user.id, user.email)
    response = unauth_client.post(
        "/users/", json={"email": test_user.email, "password": test_user.password}
    )
    users = crud.get_users(db)

    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
    assert response.json() == {
        "id": 4,
        "email": test_user.email,
        "is_active": True,
        "is_admin": None,
    }


def test_create_user_exists(unauth_client, users, test_user_exists, db):
    users = crud.get_users(db)
    for user in users:
        print(user.id, user.email)
    response = unauth_client.post(
        "/users/", json={"email": test_user_exists.email, "password": test_user_exists.password}
    )
    users = crud.get_users(db)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
