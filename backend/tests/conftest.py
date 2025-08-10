"""Test configuration for pytest."""

import os
import sys
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Patch JSONB before importing app modules
import sqlalchemy.dialects.postgresql
from tests.utils.db_utils import JSONBSQLite

# Override the JSONB type with our SQLite compatible version
sqlalchemy.dialects.postgresql.JSONB = JSONBSQLite

from app.core.security import create_access_token, get_password_hash
from app.models import User
from app.api.deps import get_db
from app.main import app
from datetime import timedelta
import uuid

# Use SQLite for tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
)


# This fixture creates the test database and tables before each test
# and drops them after the test completes
@pytest.fixture(scope="function")
def db_session() -> Generator:
    """
    Create a fresh database session for each test.
    """
    SQLModel.metadata.create_all(bind=engine)

    # Create a new session for the test
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
            # Drop all tables after the test finishes
            SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """
    Create a test client with the test database session.
    """

    # Override the get_db dependency to use our test database
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    # Clear any overrides after the test
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def test_user_headers(client) -> Dict[str, str]:
    """
    Create a test user and get authentication headers.
    """
    test_user_id = uuid.uuid4()

    with Session(engine) as db:
        user = User(
            id=test_user_id,
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            full_name="Test User",
            is_active=True,
            is_superuser=False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create a test user token
    access_token = create_access_token(
        subject=test_user_id,
        expires_delta=timedelta(minutes=30),
    )

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
def test_admin_headers(client) -> Dict[str, str]:
    """
    Create a test admin and get authentication headers.
    """
    test_admin_id = uuid.uuid4()

    with Session(engine) as db:
        user = User(
            id=test_admin_id,
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            full_name="Test User",
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(
        subject=test_admin_id,
        expires_delta=timedelta(minutes=30),
    )

    return {"Authorization": f"Bearer {access_token}"}
