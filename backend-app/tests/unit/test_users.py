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
    # WARNING: possible bottle neck for future changes
    assert response.json() == {
        "id": 1,
        "email": "user1@example.com",
        "is_active": True,
        "is_admin": False,
    }


def test_read_users_me_fault(unauth_client, db, users):
    response = unauth_client.get("/users/me/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


### Test update user state


def test_update_user_state_new(client, db, users):
    response = client.put("/users/me/update_state/", json={"new_state": False})
    assert response.status_code == 200
    assert response.json()["Message"] == "User status updated"


def test_update_user_state_same(client, db, users):
    response = client.put("/users/me/update_state/", json={"new_state": True})
    assert response.status_code == 404
    assert response.json()["detail"] == "User is_active is set to True already!"


def test_update_user_state_bad(unauth_client, db, users):
    response = unauth_client.put("/users/me/update_state/", json={"new_state": True})
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


### Test read users
def test_read_users_all(client_admin, db, users):
    response = client_admin.get("/users/users")
    assert response.status_code == 200
    assert len(response.json()) == 3


### TODO: check if necessary, since functionality already tested
def test_read_users_skip(client_admin, db, users):
    response = client_admin.get("/users/users", params={"skip": 1})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_users_limit(client_admin, db, users):
    response = client_admin.get("/users/users", params={"limit": 1})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_users_skip_limit(client_admin, db, users):
    response = client_admin.get("/users/users", params={"skip": 1, "limit": 2})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_users_unauth(client, db, users):
    response = client.get("/users/users")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


### Test read user by id
def test_read_user_by_id_ok(client_admin, db, users):
    response = client_admin.get("/users/id/1")
    assert response.status_code == 200
    # WARNING: possible bottle neck for future changes
    assert response.json() == {
        "id": 1,
        "email": "user1@example.com",
        "is_active": True,
        "is_admin": None,
    }


def test_read_user_by_id_bad(client_admin, db, users):
    response = client_admin.get("/users/id/4")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


### Test read user by mail
def test_read_user_by_mail_ok(client_admin, db, users):
    response = client_admin.get("/users/mail/user1@example.com")
    assert response.status_code == 200
    # WARNING: possible bottle neck for future changes
    assert response.json() == {
        "id": 1,
        "email": "user1@example.com",
        "is_active": True,
        "is_admin": None,
    }


def test_read_user_by_mail_bad(client_admin, db, users):
    response = client_admin.get("/users/mail/user4@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


### Test promote to admin
def test_promote_to_admin_ok(client_admin, db, users):
    response = client_admin.put("/users/1/update_admin/")

    assert response.status_code == 200
    # WARNING: possible bottle neck for future changes
    assert response.json() == {
        "id": 1,
        "email": "user1@example.com",
        "is_active": True,
        "is_admin": True,
    }


def test_promote_to_admin_not_found(client_admin, db, users):
    response = client_admin.put("/users/4/update_admin/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_promote_to_admin_is_admin(client_admin, db, users):
    response = client_admin.put("/users/2/update_admin/")
    assert response.status_code == 404
    assert response.json()["detail"] == "User is already admin"


### Test update_state_by_id
def test_update_any_user_state_ok(client_admin, db, users):
    response = client_admin.put("/users/1/update_state/", json={"new_state": False})
    updated_user = crud.get_user(db, 1)
    assert response.status_code == 200
    assert response.json()["Message"] == "User status updated"
    assert False == updated_user.is_active


def test_update_any_user_state_not_found(client_admin, db, users):
    response = client_admin.put("/users/4/update_state/", json={"new_state": False})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_any_user_state_same_state(client_admin, db, users):
    response = client_admin.put("/users/1/update_state/", json={"new_state": True})
    assert response.status_code == 404
    assert response.json()["detail"] == "User is_active is set to True already!"
