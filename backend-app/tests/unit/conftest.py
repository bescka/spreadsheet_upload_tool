from fastapi.testclient import TestClient
import pytest
from app.sql_db.database import Base
from app.models.user import UserCreate
from app.models.database import User as db_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.api.auth import get_current_active_user


@pytest.fixture(scope="session")
def test_db():
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    # Create tables in the database
    Base.metadata.create_all(engine)

    # Create a sessionmaker bound to the engine
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    session = Session()

    session.add(
        db_user(
            id=1,
            email="user1@example.com",
            hashed_password="testfake_hash",
            is_active=True,
            is_admin=True,
        )
    )
    session.add(
        db_user(
            id=2,
            email="user2@example.com",
            hashed_password="test2fake_hash",
            is_active=True,
            is_admin=False,
        )
    )
    session.add(
        db_user(
            id=3,
            email="user3@example.com",
            hashed_password="test3fake_hash",
            is_active=False,
            is_admin=False,
        )
    )

    session.commit()
    # Return a session to the test database
    yield session


@pytest.fixture(scope="function")
def test_user():
    return UserCreate(email="test@example.com", password="testpassword")


@pytest.fixture(scope="function")
def test_user_exists():
    return UserCreate(email="user1@example.com", password="testpassword")


@pytest.fixture(scope="function")
def client(test_db):
    app.dependency_overrides[get_current_active_user] = lambda: db_user(
        id=1,
        email="user1@example.com",
        hashed_password="testfake_hash",
        is_active=True,
        is_admin=True,
    )
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def bad_client(test_db):
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}
