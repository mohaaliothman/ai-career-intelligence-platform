from src.database.connection import get_db_session
from src.database.models import Job
from src.database.repositories.job_repository import JobRepository


def main() -> None:
    job_url = "https://example.com/jobs/context-manager-test"

    with get_db_session() as session:
        repository = JobRepository(session)

        saved_job = repository.get_by_source_url(job_url)

        if saved_job is None:
            print("Job was not found.")
            return

        print(f"Found ID: {saved_job.id}")
        print(f"Title: {saved_job.title}")
        print(f"Source: {saved_job.source_name}")


if __name__ == "__main__":
    main()