from src.database.connection import get_db_session
from src.scraper.job_ingestion import ingest_jobs
from src.scraper.models import ScrapedJob


jobs = [
    ScrapedJob(
        title="AI Engineer",
        company_name="Test Company",
        location="Remote",
        source_name="manual-test",
        source_url="https://example.com/jobs/ingestion-test",
    )
]


with get_db_session() as session:
    processed_count = ingest_jobs(session, jobs)

    print("Processed jobs:", processed_count)