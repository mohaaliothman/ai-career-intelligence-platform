from collections.abc import Generator 
from contextlib import contextmanager

from sqlalchemy import create_engine # It is the function that creates the SQLAlchemy Engine using the Database URL.
from sqlalchemy.orm import Session, sessionmaker
# Session = It's the type I'm working with it 
# sessionmaker = It is the factory that creates Sessions with the same settings every time.

from src.config.database import database_settings

engine = create_engine(
    database_settings.url,
    pool_pre_ping=True,
)

SessionFactory = sessionmaker(
    bind= engine,             # Each session created by the factory will use the engine of the ai_career database.
    class_= Session,          # We specify the type of object that the factory will create.
    autoflush= False,         # Prevents automatic flushing before certain queries.
    expire_on_commit= False,  # It keeps the values ​​of ORM objects available after commit.
)

# Session mangement
@contextmanager
def get_db_session() -> Generator[Session, None , None]:
    session = SessionFactory()       # Create new session

    try :
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise      # Because we don't want to hide the mistake
    finally:
        session.close()