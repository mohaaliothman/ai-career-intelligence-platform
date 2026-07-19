"""Shared foundation for database repository classes"""

from typing import Any 

from sqlalchemy.orm import Session  #We import the Session type so that we can clearly define what should be passed to the Repository.


class BaseRepository:       # This is the common origin from which specialized repositories will inherit.
    """Provide shared database operations for repository classes """

        # This property is for use within BaseRepository and subclasses, and is not a public part of the class interface.
    def __init__(self, session: Session) -> None:
        self._session = session

    def _add(self, obj:Any) -> Any : # Why we use _add not add = because it isn't public API
        """ Add an ORM object to the current transaction and flush it """
        self._session.add(obj)
        self._session.flush()

        return obj
