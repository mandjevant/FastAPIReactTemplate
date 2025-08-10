from fastapi import HTTPException, status
from sqlmodel import Session, select, func
import datetime
import uuid
from typing import Optional

from app.models import UpdatePassword, User
from app.core.security import get_password_hash, verify_password
from app.models import UserCreate, UserUpdate


class UserService:
    """Service class for user-related operations."""

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user.

        Parameters
        ----------
        db : Session
            Database session.
        user_create : UserCreate
            User creation data.

        Returns
        -------
        User
            The created user.
        """
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: uuid.UUID, user_update: UserUpdate) -> User:
        """Update user information.

        Parameters
        ----------
        db : Session
            Database session.
        user_id : uuid.UUID
            The user's ID.
        user_update : UserUpdate
            Update data for the user.

        Returns
        -------
        User
            The updated user.

        Raises
        ------
        HTTPException
            If the user is not found.
        """
        db_user = db.get(User, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "new_password":
                password = update_data["new_password"]
                hashed_password = get_password_hash(password)
                setattr(db_user, "hashed_password", hashed_password)
            else:
                setattr(db_user, field, value)

        db_user.updated_at = datetime.datetime.now(datetime.timezone.utc)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user.

        Parameters
        ----------
        db : Session
            Database session.
        email : str
            User's email address.
        password : str
            User's password.

        Returns
        -------
        Optional[User]
            The authenticated user or None if authentication fails.
        """
        user = db.exec(select(User).where(User.email == email)).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def update_password(
        db: Session,
        user: User,
        password_update: UpdatePassword,
    ) -> bool:
        """Update a user's password.

        Parameters
        ----------
        db : Session
            Database session.
        user : User
            The user whose password is being updated.
        password_update : UserUpdate
            The update object containing current and new password.

        Returns
        -------
        bool
            True if the password was updated successfully.

        Raises
        ------
        HTTPException
            If the current password is incorrect.
        """
        if not verify_password(password_update.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )

        hashed_password = get_password_hash(password_update.new_password)
        user.hashed_password = hashed_password
        db.add(user)
        db.commit()
        return True

    @staticmethod
    def delete_user(
        db: Session,
        user: User,
    ) -> bool:
        """Delete a user from the database.

        Parameters
        ----------
        db : Session
            Database session.
        user : User
            The user to delete.

        Returns
        -------
        bool
            True if the user was deleted successfully.
        """
        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def read_user(
        db: Session,
        user_id: uuid.UUID,
    ) -> Optional[User]:
        """Get a user by their unique ID.

        Parameters
        ----------
        db : Session
            Database session.
        user_id : uuid.UUID
            The user's unique ID.

        Returns
        -------
        Optional[User]
            The user if found.

        Raises
        ------
        HTTPException
            If the user is not found.
        """
        user = db.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    @staticmethod
    def list_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        """List users with pagination.

        Parameters
        ----------
        db : Session
            Database session.
        skip : int
            Number of users to skip (for pagination).
        limit : int
            Maximum number of users to return.

        Returns
        -------
        list[User]
            List of users for the current page.
        """
        users = db.exec(select(User).offset(skip).limit(limit)).all()
        return list(users)

    @staticmethod
    def list_users_count(
        db: Session,
    ) -> int:
        """Count the total number of users in the database.

        Parameters
        ----------
        db : Session
            Database session.

        Returns
        -------
        int
            Total number of users.
        """
        return db.exec(select(func.count()).select_from(User)).one()
