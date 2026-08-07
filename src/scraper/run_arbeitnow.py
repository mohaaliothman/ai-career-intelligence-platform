from src.database.connection import get_db_session
from src.scraper.job_ingestion import ingest_jobs
from src.scraper.sources.arbeitnow_scraper import ArbeitnowScraper


def main() -> None:
    scraper = ArbeitnowScraper()

    jobs = scraper.scrape()

    print(f"Collected {len(jobs)} jobs")

    with get_db_session() as session:
        processed_count = ingest_jobs(session, jobs)

    print(f"Processed jobs: {processed_count}")


if __name__ == "__main__":
    main()