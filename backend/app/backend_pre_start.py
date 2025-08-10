import logging

from sqlalchemy import Engine
from sqlmodel import Session, select, SQLModel
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.db import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    """Try to initialize a database session to check if the DB is awake.

    Parameters
    ----------
    db_engine : Engine
        SQLAlchemy engine to use for the session.

    Raises
    ------
    Exception
        If the database is not available after retries.
    """
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    """Main entry point for backend pre-start script.

    Logs the initialization process and checks DB readiness.
    """
    logger.info("Initializing service")
    init(engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
