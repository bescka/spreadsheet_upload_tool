from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from app.api.auth import authenticate_user, create_access_token


def test_authenticate_user_success(mock_db, mock_get_user_by_email_success, mock_user, monkeypatch):
    """Test successful user authentication."""

    def mock_verify_password(password, hashed_password):
        return True

    # Monkeypatching external dependencies
    monkeypatch.setattr("app.api.auth.get_user_by_email", mock_get_user_by_email_success)
    monkeypatch.setattr("app.api.auth.verify_password", mock_verify_password)

    # Call the function
    result = authenticate_user("user1@example.com", "test1", db=mock_db)
    print(result)

    # Assert that authentication was successful and returns the user
    assert result == mock_user


def test_authenticate_user_wrong_password(mock_db, mock_get_user_by_email_success, monkeypatch):
    """Test user authentication with wrong password."""

    def mock_verify_password(password, hashed_password):
        return False

    # Monkeypatching external dependencies
    monkeypatch.setattr("app.api.auth.get_user_by_email", mock_get_user_by_email_success)
    monkeypatch.setattr("app.api.auth.verify_password", mock_verify_password)

    # Call the function
    result = authenticate_user("test@example.com", "wrong_password", db=mock_db)

    # Assert that authentication fails
    assert result is False


def test_authenticate_user_no_user_found(mock_db, mock_get_user_by_email_none, monkeypatch):
    """Test user authentication when no user is found."""

    # Monkeypatching external dependencies
    monkeypatch.setattr("app.api.auth.get_user_by_email", mock_get_user_by_email_none)

    # Call the function
    result = authenticate_user("unknown@example.com", "password", db=mock_db)

    # Assert that authentication fails
    assert result is False


def test_create_access_token(mock_user, monkeypatch):
    TEST_SECRET_KEY = "SECRET"
    monkeypatch.setattr("app.api.auth.SECRET_KEY", TEST_SECRET_KEY)

    expires_delta = timedelta(minutes=1)
    access_token = create_access_token(data={"sub": mock_user.email}, expires_delta=expires_delta)
    decoded_token = jwt.decode(access_token, TEST_SECRET_KEY, algorithms=["HS256"])

    # Assert the sub claim is correct
    assert decoded_token["sub"] == mock_user.email

    # Assert the expiration time is correct and within a reasonable range
    exp_time = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
    now_time = datetime.now(timezone.utc)

    # Token should expire in approximately the given expiration delta
    assert now_time < exp_time <= (now_time + expires_delta + timedelta(seconds=2))


def test_create_access_token_default_expiration(mock_user, monkeypatch):
    TEST_SECRET_KEY = "SECRET"
    monkeypatch.setattr("app.api.auth.SECRET_KEY", TEST_SECRET_KEY)

    # Call create_access_token without specifying expires_delta
    access_token = create_access_token(data={"sub": mock_user.email})

    decoded_token = jwt.decode(access_token, TEST_SECRET_KEY, algorithms=["HS256"])

    # Assert the sub claim is correct
    assert decoded_token["sub"] == mock_user.email

    # Assert the default expiration is 15 minutes
    exp_time = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
    now_time = datetime.now(timezone.utc)
    assert now_time < exp_time <= (now_time + timedelta(minutes=15) + timedelta(seconds=2))


def test_create_access_token_expired_token(mock_user, monkeypatch):
    TEST_SECRET_KEY = "SECRET"
    monkeypatch.setattr("app.api.auth.SECRET_KEY", TEST_SECRET_KEY)

    # Create an expired token by setting expires_delta to -1 minute
    access_token = create_access_token(
        data={"sub": mock_user.email}, expires_delta=timedelta(minutes=-1)
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(access_token, TEST_SECRET_KEY, algorithms=["HS256"])
