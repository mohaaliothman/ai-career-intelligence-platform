"""Save scraped job records into the database."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.database.models import Job
from src.database.repositories.job_repository import JobRepository
from src.scraper.models import ScrapedJob


def ingest_jobs(
    session: Session,
    scraped_jobs: list[ScrapedJob],
) -> int:
    """Insert or update scraped jobs and return the processed count."""

    repository = JobRepository(session)

    processed_count = 0

    for scraped_job in scraped_jobs:
        job = Job(
            title=scraped_job.title,
            company_name=scraped_job.company_name,
            location=scraped_job.location,
            employment_type=scraped_job.employment_type,
            experience_level=scraped_job.experience_level,
            salary_min=scraped_job.salary_min,
            salary_max=scraped_job.salary_max,
            salary_currency=scraped_job.salary_currency,
            description=scraped_job.description,
            source_name=scraped_job.source_name,
            source_url=scraped_job.source_url,
            posted_at=scraped_job.posted_at,
            scraped_at=scraped_job.scraped_at
            or datetime.now(timezone.utc),  # Because scraped_at in ScrapedJob is optional, while the database does not allow it to be NULL
        )                                   # We used upsert() so that the functions would not be duplicated when the summation was run again

        repository.upsert(job)
        processed_count += 1

    return processed_count