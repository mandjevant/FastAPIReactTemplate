"""Test security module."""

import jwt
from jwt.exceptions import InvalidTokenError
import pytest
from datetime import datetime, timedelta, timezone
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    ALGORITHM,
    verify_token,
)
from app.core.config import settings


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword"  # pragma: allowlist secret
    hashed = get_password_hash(password)

    # Hash should be different from original password
    assert hashed != password

    # Verify should return True for correct password
    assert verify_password(password, hashed) is True

    # Verify should return False for incorrect password
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "test@example.com", "user_id": "12345"}
    token = create_access_token(subject=data, expires_delta=timedelta(minutes=30))

    # Token should be a string
    assert isinstance(token, str)

    # Token should be decodable with our secret key
    decoded = jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    # Check if the data is preserved in the token
    assert decoded["sub"] == str(data)

    # Check if the expiration date is set
    assert "exp" in decoded


def test_create_access_token_with_expiration():
    """Test JWT token creation with custom expiration."""
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)

    token = create_access_token(
        subject=data, expires_delta=expires_delta
    )  # Decode the token
    decoded = jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    # Calculate expected expiration time (with small tolerance for test execution time)
    expected_exp = datetime.now(timezone.utc) + expires_delta

    # Verify the expiration time (with a small tolerance)
    assert (
        abs(decoded["exp"] - expected_exp.timestamp()) < 10
    )  # Allow 10 seconds tolerance


def test_verify_token():
    """Test token verification."""
    data = {"sub": "test@example.com", "user_id": "12345"}
    token = create_access_token(
        subject=data, expires_delta=timedelta(minutes=30)
    )  # Valid token should be verified successfully
    payload = verify_token(token)
    # Since we store data as string in the token, we compare with stringified version
    assert payload["sub"] == str(data)

    # Manipulated token should fail verification
    invalid_token = token[:-5] + "12345"
    with pytest.raises(InvalidTokenError):
        verify_token(invalid_token)

    # Expired token should fail verification
    expired_token = create_access_token(
        subject=data, expires_delta=timedelta(seconds=-1)  # Already expired
    )

    with pytest.raises(InvalidTokenError):
        verify_token(expired_token)
