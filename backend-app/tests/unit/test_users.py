from fastapi.testclient import TestClient
from app.api import users
from app.sql_db import crud


def test_create_user_first(unauth_client, test_user, db):
    response = unauth_client.post(
        "/users/", json={"email": test_user.email, "password": test_user.password}
    )

    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
    assert response.json() == {
        "id": 1,
        "email": test_user.email,
        "is_active": True,
        "is_admin": None,
    }


def test_create_user_additional(unauth_client, users, test_user, db):
    response = unauth_client.post(
        "/users/", json={"email": test_user.email, "password": test_user.password}
    )

    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
    assert response.json() == {
        "id": 4,
        "email": test_user.email,
        "is_active": True,
        "is_admin": None,
    }


def test_create_user_exists(unauth_client, users, test_user_exists, db):
    response = unauth_client.post(
        "/users/", json={"email": test_user_exists.email, "password": test_user_exists.password}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_read_users_me_ok(client, db, users):
    response = client.get("/users/me/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "user1@example.com",
        "is_active": True,
        "is_admin": True,
    }


def test_read_users_me_fault(unauth_client, db, users):
    response = unauth_client.get("/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
