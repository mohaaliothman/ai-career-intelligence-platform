from sqlalchemy import text

from src.database.connection import get_db_session


with get_db_session() as session:
    result = session.execute(text("SELECT 1"))

    print("Database connection successful:", result.scalar_one())