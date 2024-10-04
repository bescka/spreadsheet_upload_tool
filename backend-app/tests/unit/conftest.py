from io import BytesIO
from unittest.mock import MagicMock

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.api.auth import get_current_active_admin, get_current_active_user, get_user_by_email
from app.main import app
from app.models import user as api_m
from app.models.database import User as db_user
from app.models.file_db import create_file_table_class, update_schema
from app.models.user import UserCreate, UserInDB
from app.sql_db.crud import create_user, get_db, update_is_active, update_is_admin
from app.sql_db.database import Base
from app.sql_db.file_crud import create_update_table, insert_data


@pytest.fixture(scope="session")
def db_engine():

    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    # Create tables in the database
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db(db_engine):
    with db_engine.connect() as connection:
        transaction = connection.begin()
        db = Session(autocommit=False, autoflush=False, bind=connection)
        yield db
        transaction.rollback()
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
        hashed_password="test1fake_hash",
        is_active=True,
        is_admin=False,
    )
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def client_admin(db):
    app.dependency_overrides[get_current_active_admin] = lambda: db_user(
        id=2,
        email="user2@example.com",
        hashed_password="test2fake_hash",
        is_active=True,
        is_admin=True,
    )
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def unauth_client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def users(db):
    create_user(db, api_m.UserCreate(email="user1@example.com", password="test1"))
    create_user(db, api_m.UserCreate(email="user2@example.com", password="test2"))
    # HACK: Change in future
    user2 = get_user_by_email(db, email="user2@example.com")
    update_is_admin(db, user2)
    create_user(db, api_m.UserCreate(email="user3@example.com", password="test3"))
    user3 = get_user_by_email(db, email="user3@example.com")
    update_is_active(db, user3, new_state=False)


@pytest.fixture(scope="function")
def file_db(db, files_good):

    df = pd.read_csv(BytesIO(files_good["file"][1].encode()))
    engine = db.get_bind().engine
    filetable, msg = create_update_table(df, engine, "file_table")

    insert_data(db, df, filetable)


@pytest.fixture(scope="function")
def files_good():
    files = {
        "file": (
            "test.csv",
            "name,email,person_id,01.01.2024,02.01.2024\ntim, tim@kh.de,1,2,5\nmax, max@kh.de,2,3,20\ntina, tina@kh.de,3,30,2",
        )
    }
    return files


@pytest.fixture(scope="function")
def df_files_good(files_good):
    df = pd.read_csv(BytesIO(files_good["file"][1].encode()))
    return df


@pytest.fixture(scope="function")
def file_table_good(df_files_good, db_engine):
    file_table, msg = create_update_table(df_files_good, db_engine, "file_table")
    return file_table


@pytest.fixture(scope="function")
def files_good_updated():
    files = {
        "file": (
            "test.csv",
            "name,email,person_id,01.01.2024,02.01.2024,03.01.2024\ntim, tim@kh.de,1,2,5,12\nmax, max@kh.de,2,3,20,20\ntina, tina@kh.de,3,30,2,3",
        )
    }
    return files


@pytest.fixture(scope="function")
def df_files_good_updated(files_good_updated):
    df = pd.read_csv(BytesIO(files_good_updated["file"][1].encode()))
    return df


@pytest.fixture(scope="function")
def files_bad_type():
    files = {
        "file": (
            "test.txt",
            "name,email,_person_id,01.01.2024,02.01.2024\ntim, tim@kh.de,1,2,5\nmax, max@kh.de,test,3,20\ntina, tina@kh.de,3,30,2",
        )
    }
    return files


@pytest.fixture(scope="function")
def files_bad_dtype():
    files = {
        "file": (
            "test.csv",
            "name,email,_person_id,01.01.2024,02.01.2024\ntim, tim@kh.de,1,2,5\nmax, max@kh.de,test,3,20\ntina, tina@kh.de,3,30,2",
        )
    }
    return files


@pytest.fixture(scope="function")
def files_bad_column():
    files = {
        "file": (
            "test.csv",
            "fullname,email,person_id,01.01.2024,02.01.2024\ntim, tim@kh.de,1,2,5\nmax, max@kh.de,test,3,20\ntina, tina@kh.de,3,30,2",
        )
    }
    return files


@pytest.fixture
def mock_db():
    """Fixture for mocking the database session."""
    db = MagicMock(spec=Session)
    return db


@pytest.fixture
def mock_user():
    """Fixture for mocking a user."""
    user = UserInDB(email="user1@example.com", password="test1", hashed_password="test1fake_hash")
    return user


@pytest.fixture
def mock_get_user_by_email_success(mock_user):
    """Fixture for mocking get_user_by_email to retuern the mock user."""

    def mock_get_user_by_email(db, email):
        return mock_user

    return mock_get_user_by_email


@pytest.fixture
def mock_get_user_by_email_none():
    """Fixture for mocking get_user_by_email to retuern None (user not found)."""

    def mock_get_user_by_email(db, email):
        return None

    return mock_get_user_by_email
