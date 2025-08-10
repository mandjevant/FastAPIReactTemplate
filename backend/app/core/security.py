from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    """Create a JWT access token.

    Parameters
    ----------
    subject : str | Any
        The subject (user id or similar) to encode.
    expires_delta : timedelta
        Expiry duration for the token.

    Returns
    -------
    str
        Encoded JWT token.
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """Verify a JWT token and return its payload.

    Parameters
    ----------
    token : str
        The token to verify.

    Returns
    -------
    dict
        The decoded token payload.

    Raises
    ------
    jwt.PyJWTError
        If token is invalid.
    """
    return jwt.decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=[ALGORITHM],
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash.

    Parameters
    ----------
    plain_password : str
        The plain password.
    hashed_password : str
        The hashed password.

    Returns
    -------
    bool
        True if the password matches, else False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storage.

    Parameters
    ----------
    password : str
        The plain password.

    Returns
    -------
    str
        The hashed password.
    """
    return pwd_context.hash(password)
