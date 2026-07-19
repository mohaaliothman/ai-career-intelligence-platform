""" Run the Remotive scraper and save jobs to the database """

from src.database.connection import get_db_session
from src.scraper.job_ingestion import ingest_jobs
from src.scraper.sources.remotive_scraper import RemotiveScraper


def main() -> None:
    """ Run the complete scraping pipeline """

    scraper = RemotiveScraper()

    jobs = scraper.scrape()

    print(f"collected {len(jobs)} jobs ")

    with get_db_session() as session:
        processed = ingest_jobs(session, jobs)

    print(f"Saved {processed} jobs ")

if __name__ == "__main__":
    main()