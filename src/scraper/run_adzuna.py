"""Run the Adzuna scraper and save jobs to the database."""

from src.database.connection import get_db_session
from src.scraper.job_ingestion import ingest_jobs
from src.scraper.sources.adzuna_scraper import AdzunaScraper


def main() -> None:
    """Run the complete Adzuna scraping pipeline."""

    scraper = AdzunaScraper()

    jobs = scraper.scrape()

    print(f"Collected {len(jobs)} jobs")

    with get_db_session() as session:
        processed = ingest_jobs(session, jobs)

    print(f"Processed {processed} jobs")


if __name__ == "__main__":
    main()