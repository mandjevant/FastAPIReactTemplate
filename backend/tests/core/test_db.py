"""Test database connection and session creation."""

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel

from app.core.db import engine


@pytest.fixture
def db_session():
    """Create and yield a database session for testing."""
    # Create an in-memory SQLite database for testing
    test_engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session


def test_engine_creation():
    """Test that the database engine is created properly."""
    assert isinstance(engine, Engine)
