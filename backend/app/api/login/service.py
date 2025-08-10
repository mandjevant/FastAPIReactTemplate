from sqlmodel import Session, select

from app.models import User

from app.core.security import verify_password


class LoginService:
    """Service class for login/authentication operations."""

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User | None:
        """Authenticate a user by email and password.

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
        User | None
            The authenticated user or None if authentication fails.
        """
        db_user = LoginService.get_user_by_email(db=db, email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Get a user by email address.

        Parameters
        ----------
        db : Session
            Database session.
        email : str
            User's email address.

        Returns
        -------
        User | None
            The user if found, else None.
        """
        statement = select(User).where(User.email == email)
        session_user = db.exec(statement).first()
        return session_user
