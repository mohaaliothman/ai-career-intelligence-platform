""" Database access operation for job records """

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Job
from src.database.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository):
    """ Provide database operations related to jobs """

    def __init__(self, session:Session) -> None:
        super().__init__(session)

    def get_by_source_url(self, source_url: str) -> Job | None :
        """ Return the job matching the source URL, or None if it does not exist """
        statement = select(Job).where(Job.source_url == source_url)

        """This like :  SELECT *
                        FROM jobs
                        WHERE source_url = :source_url; """

        return self._session.scalar(statement) #scalar() executes the query and returns the first ORM value from the first row.
        

    def create(self, job: Job) -> Job:
        """ Add a new job to the current database transaction """
        self._session.add(job)
        self._session.flush()

        return job