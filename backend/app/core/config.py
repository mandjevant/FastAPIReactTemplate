import secrets
import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self
import logging


def parse_cors(v: Any) -> list[str] | str:
    """Parse CORS origins from a string or list.

    Parameters
    ----------
    v : Any
        The value to parse.

    Returns
    -------
    list[str] | str
        List of origins or the original value.
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file.

    Attributes
    ----------
    API_V1_STR : str
        API version prefix.
    SECRET_KEY : str
        Secret key for cryptography.
    ACCESS_TOKEN_EXPIRE_MINUTES : int
        Access token expiry in minutes.
    FRONTEND_HOST : str
        Frontend host URL.
    ENVIRONMENT : Literal["local", "staging", "production"]
        Deployment environment.
    BACKEND_CORS_ORIGINS : list[AnyUrl] | str
        Allowed CORS origins.
    PROJECT_NAME : str
        Project name.
    SENTRY_DSN : HttpUrl | None
        Sentry DSN for error tracking.
    POSTGRES_SERVER : str
        Postgres server address.
    POSTGRES_PORT : int
        Postgres port.
    POSTGRES_USER : str
        Postgres username.
    POSTGRES_PASSWORD : str
        Postgres password.
    POSTGRES_DB : str
        Postgres database name.
    SQLALCHEMY_DATABASE_URI : PostgresDsn
        SQLAlchemy database URI (computed).
    EMAIL_TEST_USER : EmailStr
        Test user email.
    FIRST_SUPERUSER : EmailStr
        First superuser email.
    FIRST_SUPERUSER_PASSWORD : str
        First superuser password.
    """

    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        """Return all allowed CORS origins including the frontend host."""
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """Return the SQLAlchemy database URI for Postgres."""
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """Warn or raise if a secret is set to the default insecure value."""
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """Enforce that critical secrets are not set to insecure defaults."""
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )
        return self


settings = Settings()  # type: ignore
