from src.database.connection import get_db_session
from src.database.models import Job
from src.database.repositories.job_repository import JobRepository


SOURCE_URL = "https://example.com/jobs/upsert-test"


with get_db_session() as session:
    repository = JobRepository(session)

    first_job = Job(
        title="Junior Data Analyst",
        company_name="Test Company",
        source_name="manual-test",
        source_url=SOURCE_URL,
    )

    created_job = repository.upsert(first_job)

    print("First operation ID:", created_job.id)
    print("First title:", created_job.title)


with get_db_session() as session:
    repository = JobRepository(session)

    updated_job = Job(
        title="Updated Data Analyst",
        company_name="Updated Test Company",
        source_name="manual-test",
        source_url=SOURCE_URL,
    )

    result = repository.upsert(updated_job)

    print("Second operation ID:", result.id)
    print("Updated title:", result.title)
    print("Updated company:", result.company_name)