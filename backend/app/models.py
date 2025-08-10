from typing import List, Any, Optional
from datetime import datetime
import uuid
from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import Mapped

# ----------------------
# Base Models & Enums
# ----------------------


class Message(BaseModel):
    """Standard message response.

    Attributes
    ----------
    message : str
        The message string.
    """

    message: str


class ErrorMessage(BaseModel):
    """Standard error response.

    Attributes
    ----------
    detail : str
        The error detail string.
    """

    detail: str


class UserRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    GUEST = "guest"


# ----------------------
# Core Database Models
# ----------------------


class User(SQLModel, table=True):  # type: ignore[call-arg]
    """User database model.

    Attributes
    ----------
    id : uuid.UUID
        Primary key.
    email : EmailStr
        User's email address.
    hashed_password : str
        Hashed password.
    full_name : Optional[str]
        Full name of the user.
    avatar_url : Optional[str]
        Avatar image URL.
    phone : Optional[str]
        Phone number.
    is_active : bool
        Whether the user is active.
    is_superuser : bool
        Whether the user is a superuser.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    settings : List[UserSetting]
        User settings relationship.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    settings: Mapped[List["UserSetting"]] = Relationship(back_populates="user")


class UserSetting(SQLModel, table=True):  # type: ignore[call-arg]
    """User setting database model.

    Attributes
    ----------
    id : uuid.UUID
        Primary key.
    user_id : uuid.UUID
        Foreign key to user.
    setting_key : str
        The key for the setting.
    setting_value : str
        The value for the setting.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    setting_key: str
    setting_value: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    user: Mapped["User"] = Relationship(back_populates="settings")


class Note(SQLModel, table=True):  # type: ignore[call-arg]
    """A note belonging to a user.

    Attributes
    ----------
    id : int
        Primary key.
    title : str
        Title of the note.
    content : str
        Content of the note.
    user_id : uuid.UUID
        Foreign key to the user who owns the note.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    """

    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# ----------------------
# Request/Response Models
# ----------------------


class Token(SQLModel):
    """Access token response model.

    Attributes
    ----------
    access_token : str
        The JWT access token.
    token_type : str
        The type of token (default: "bearer").
    """

    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    """Token payload for authentication.

    Attributes
    ----------
    sub : str | None
        Subject (user id) from the token.
    """

    sub: str | None = None


class UserBase(SQLModel):
    """Base user model for shared fields.

    Attributes
    ----------
    email : EmailStr
        User's email address.
    full_name : str | None
        Full name of the user.
    is_active : bool
        Whether the user is active.
    is_superuser : bool
        Whether the user is a superuser.
    """

    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """User creation model.

    Attributes
    ----------
    password : str
        The user's password.
    """

    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    """User registration model.

    Attributes
    ----------
    email : EmailStr
        User's email address.
    password : str
        The user's password.
    full_name : str | None
        Full name of the user.
    """

    email: EmailStr
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = None


class UserPublic(UserBase):
    """Public user model for API responses.

    Attributes
    ----------
    id : uuid.UUID
        User's unique ID.
    email : EmailStr
        User's email address.
    full_name : str | None
        Full name of the user.
    is_active : bool
        Whether the user is active.
    is_superuser : bool
        Whether the user is a superuser.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    """

    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime


class UserLite(UserBase):
    """Lite user model for lightweight responses.

    Attributes
    ----------
    id : uuid.UUID
        User's unique ID.
    email : EmailStr
        User's email address.
    full_name : str | None
        Full name of the user.
    is_active : bool
        Whether the user is active.
    is_superuser : bool
        Whether the user is a superuser.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    """

    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime


class UsersPublic(SQLModel):
    """Paginated list of public users.

    Attributes
    ----------
    data : List[UserPublic]
        List of user objects.
    count : int
        Total number of users.
    """

    data: List[UserPublic]
    count: int


class UserUpdate(SQLModel):
    """User update model for PATCH/PUT requests.

    Attributes
    ----------
    email : EmailStr | None
        New email address.
    full_name : str | None
        New full name.
    avatar_url : str | None
        New avatar URL.
    phone : str | None
        New phone number.
    password : str | None
        New password.
    is_active : bool
        Whether the user is active.
    is_superuser : bool
        Whether the user is a superuser.
    """

    email: EmailStr | None = Field(default=None, max_length=255)
    full_name: str | None = None
    avatar_url: str | None = None
    phone: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=40)
    is_active: bool = True
    is_superuser: bool = False


class UpdatePassword(SQLModel):
    """Model for updating a user's password.

    Attributes
    ----------
    current_password : str
        The user's current password.
    new_password : str
        The new password to set.
    """

    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class NewPassword(SQLModel):
    """Model for setting a new password with a token.

    Attributes
    ----------
    token : str
        The password reset token.
    new_password : str
        The new password to set.
    """

    token: str
    new_password: str = Field(min_length=8, max_length=40)


class UserSettingBase(SQLModel):
    """Base model for user settings.

    Attributes
    ----------
    setting_key : str
        The key for the setting.
    setting_value : str
        The value for the setting.
    """

    setting_key: str
    setting_value: str


class UserSettingCreate(UserSettingBase):
    """Model for creating a user setting (inherits all fields)."""

    pass


class UserSettingPublic(UserSettingBase):
    """Public user setting model for API responses.

    Attributes
    ----------
    id : uuid.UUID
        Setting unique ID.
    user_id : uuid.UUID
        User's unique ID.
    created_at : datetime
        Creation timestamp.
    updated_at : datetime
        Last update timestamp.
    """

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# ----------------------
# Pagination & Lists
# ----------------------


class PaginatedResponse(SQLModel):
    """Generic paginated response model.

    Attributes
    ----------
    data : List[Any]
        List of items for the current page.
    count : int
        Total number of items.
    page : int
        Current page number.
    pages : int
        Total number of pages.
    size : int
        Number of items per page.
    """

    data: List[Any]
    count: int
    page: int
    pages: int
    size: int


# ----------------------
# Relationship Fixes
# ----------------------

Note.model_rebuild()
