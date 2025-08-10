from sqlmodel import Session, create_engine, select, text

from app.api.users.service import UserService
from app.core.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    """Initialize the database and create the first superuser if needed.

    Parameters
    ----------
    session : Session
        SQLModel database session.
    """
    from sqlmodel import SQLModel
    import logging

    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database();"))
        logging.info("Connected to database: %s", result.scalar())

        result = conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
            )
        )
        logging.info("Existing tables: %s", [row[0] for row in result.fetchall()])

    logging.info(f"Using database URI: {settings.SQLALCHEMY_DATABASE_URI}")
    logging.info(SQLModel.metadata.tables)
    import traceback

    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        logging.error("Error creating database tables: %s", e)
        logging.error(traceback.format_exc())
        raise

    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database();"))
        logging.info("Connected to database: %s", result.scalar())

        result = conn.execute(
            text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
            )
        )
        logging.info("Existing tables: %s", [row[0] for row in result.fetchall()])

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = UserService.create_user(db=session, user_create=user_in)
