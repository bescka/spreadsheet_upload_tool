from fastapi.testclient import TestClient
import pytest
from app.sql_db.database import Base
from app.models.user import UserCreate
from app.models.database import User as db_user
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from app.main import app
from app.api.auth import get_current_active_user
from app.sql_db.crud import create_user, get_db
from app.models import user as api_m


@pytest.fixture(scope="session")
def db_engine():

    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    # Create tables in the database
    Base.metadata.create_all(engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    transaction = connection.begin()

    db = Session(autocommit=False, autoflush=False, bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_user():
    return UserCreate(email="test@example.com", password="testpassword")


@pytest.fixture(scope="function")
def test_user_exists():
    return UserCreate(email="user1@example.com", password="test1")


@pytest.fixture(scope="function")
def client(db):
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


nt = TestClient(app)


@pytest.fixture(scope="function")
def unauth_client(db):

    app.dependency_overrides[get_db] = lambda: db  # Assuming you have a get_db dependency
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def users(db):
    create_user(db, api_m.UserCreate(email="user1@example.com", password="test1"))
    create_user(db, api_m.UserCreate(email="user2@example.com", password="test2"))
    create_user(db, api_m.UserCreate(email="user3@example.com", password="test3"))
