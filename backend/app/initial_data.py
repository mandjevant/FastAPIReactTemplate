import logging

from sqlmodel import Session

from app.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """Initialize the database with initial data.

    Opens a session and calls `init_db` to create tables and the first superuser.
    """
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    """Main entry point for initial data creation script.

    Logs the process and calls `init`.
    """
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
