from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from app.api.deps import (
    SessionDep,
    get_current_user,
    get_current_active_superuser,
)
from app.models import (
    User,
    UserPublic,
    UsersPublic,
    UserUpdate,
    UpdatePassword,
    Message,
    UserCreate,
    UserRegister,
)
from app.api.users.service import UserService
from app.api.login.service import LoginService

signUpLoginRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)

# --------------------
# User Routes
# --------------------


@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    """Get the current authenticated user's public info.

    Parameters
    ----------
    current_user : User
        The current authenticated user.

    Returns
    -------
    UserPublic
        The user's public info.
    """
    return UserPublic.model_validate(current_user)


@router.patch("/me", response_model=UserPublic)
async def update_user_me(
    db: SessionDep,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> UserPublic:
    """Update the current authenticated user's info.

    Parameters
    ----------
    db : Session
        Database session.
    user_update : UserUpdate
        Update data for the user.
    current_user : User
        The current authenticated user.

    Returns
    -------
    UserPublic
        The updated user's public info.
    """
    return UserPublic.model_validate(
        UserService.update_user(db, current_user.id, user_update)
    )


@router.delete("/me", response_model=Message)
async def delete_user_me(
    db: SessionDep, current_user: User = Depends(get_current_user)
) -> Message:
    """Delete the current authenticated user.

    Parameters
    ----------
    db : Session
        Database session.
    current_user : User
        The current authenticated user.

    Returns
    -------
    Message
        Success or failure message.
    """
    if current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super users are not allowed to delete themselves",
        )
    if UserService.delete_user(db, current_user):
        return Message(message="User deleted successfully")
    return Message(message="User deletion failed")


@router.post("/me/password", response_model=Message)
async def update_password(
    db: SessionDep,
    password_update: UpdatePassword,
    current_user: User = Depends(get_current_user),
):
    if UserService.update_password(db, current_user, password_update):
        return Message(message="Password updated successfully")
    return Message(message="Password update failed")


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(
    db: SessionDep,
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
):
    user = UserService.read_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/", response_model=UsersPublic)
async def list_users(
    db: SessionDep,
    skip: int = 0,
    limit: int = 100,
    current_superuser: User = Depends(get_current_active_superuser),
):
    users = UserService.list_users(db, skip, limit)
    users_count = UserService.list_users_count(db)
    return {
        "data": users,
        "count": users_count,
    }


@router.get("/find/{email}", response_model=UserPublic)
async def find_user_by_email(
    db: SessionDep,
    email: str,
    company_admin: User = Depends(get_current_active_superuser),
):
    user = LoginService.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@signUpLoginRouter.post("/signup", response_model=UserPublic)
async def register_user(db: SessionDep, user_in: UserRegister) -> UserPublic:
    """Register a new user account.

    Parameters
    ----------
    db : Session
        Database session.
    user_in : UserRegister
        Registration data for the new user.

    Returns
    -------
    UserPublic
        The created user's public info.

    Raises
    ------
    HTTPException
        If a user with the given email already exists.
    """
    user = LoginService.get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = UserService.create_user(db=db, user_create=user_create)
    return UserPublic.model_validate(user)


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    db: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
    current_superuser: User = Depends(get_current_active_superuser),
) -> UserPublic:
    """Update a user by ID (admin/superuser only).

    Parameters
    ----------
    db : Session
        Database session.
    user_id : uuid.UUID
        The user's unique ID.
    user_in : UserUpdate
        Update data for the user.
    current_superuser : User
        The current authenticated superuser.

    Returns
    -------
    UserPublic
        The updated user's public info.

    Raises
    ------
    HTTPException
        If the user does not exist or email is already taken.
    """
    db_user = UserService.read_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = LoginService.get_user_by_email(db=db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

    db_user = UserService.update_user(db=db, user_id=user_id, user_update=user_in)
    return UserPublic.model_validate(db_user)


@router.delete("/{user_id}", response_model=Message)
def delete_user(
    db: SessionDep, user_id: uuid.UUID, current_user: User = Depends(get_current_user)
) -> Message:
    """Delete a user by ID (admin/superuser only).

    Parameters
    ----------
    db : Session
        Database session.
    user_id : uuid.UUID
        The user's unique ID.
    current_user : User
        The current authenticated user.

    Returns
    -------
    Message
        Success or failure message.

    Raises
    ------
    HTTPException
        If the user does not exist or tries to delete themselves.
    """
    user = UserService.read_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user == current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super users are not allowed to delete themselves",
        )
    UserService.delete_user(db, user)
    return Message(message="User deleted successfully")
