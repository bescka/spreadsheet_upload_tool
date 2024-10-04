from app.api.auth import authenticate_user


def test_authenticate_user_success(mock_db, mock_get_user_by_email_success, mock_user, monkeypatch):
    """Test successful user authentication."""

    def mock_verify_password():
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

    def mock_verify_password():
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
