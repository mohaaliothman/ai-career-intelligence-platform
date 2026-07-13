"""Shared foundation for database repository classes"""

from sqlalchemy.orm import Session  #We import the Session type so that we can clearly define what should be passed to the Repository.


class BaseRepository:       # This is the common origin from which specialized repositories will inherit.
    """Provide database repositories with an existing SQLAlchemy session"""

        # This property is for use within BaseRepository and subclasses, and is not a public part of the class interface.
    def __init__(self, session: Session) -> None:
        self._session = session
