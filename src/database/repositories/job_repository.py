"""Database access operations for job records."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Job
from src.database.repositories.base_repository import BaseRepository


class JobRepository(BaseRepository):
    """Provide database operations related to jobs."""

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_source_url(self, source_url: str) -> Job | None:
        """Return the job matching the source URL, or None if it does not exist."""

        statement = select(Job).where(Job.source_url == source_url)

        return self._session.scalar(statement)

    def create(self, job: Job) -> Job:
        """Add a new job to the current database transaction."""

        return self._add(job)

    def upsert(self, job: Job) -> Job:
        """Create a new job or update an existing job with the same source URL."""

        existing_job = self.get_by_source_url(job.source_url)

        if existing_job is None:
            return self.create(job)

        editable_fields = (
            "title",
            "company_name",
            "location",
            "employment_type",
            "experience_level",
            "salary_min",
            "salary_max",
            "salary_currency",
            "description",
            "source_name",
            "posted_at",
        )

        for field in editable_fields:
            setattr(existing_job, field, getattr(job, field))

        existing_job.is_active = True

        return existing_job