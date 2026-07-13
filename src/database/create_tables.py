"""Create all database tables registered in SQLAlchemy metadata."""

from sqlalchemy.exc import SQLAlchemyError

from src.database.base import Base
from src.database.connection import engine
from src.database.models.job import Job
from src.utils.logger import get_logger


logger = get_logger(__name__)


def create_tables() -> None:    #This means that the function performs an operation, but does not return a value.
    """Create all tables that do not already exist in the database."""
    try:
        logger.info("Starting database table creation.")

        Base.metadata.create_all(bind=engine) 
        # Base.metadata = All tables registered.
        # create_all = Create the tables that do not exist.
        # bind=engine = Perform the operation using the PostgreSQL Engine.

        logger.info(
            "Database tables created successfully. Registered tables: %s",
            list(Base.metadata.tables.keys()),
        )
    except SQLAlchemyError:
        logger.exception("Failed to create database tables.")
        raise


if __name__ == "__main__":
    create_tables()