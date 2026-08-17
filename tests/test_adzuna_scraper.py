from src.scraper.sources.adzuna_scraper import AdzunaScraper


def test_adzuna_scraper():
    scraper = AdzunaScraper()

    jobs = scraper.scrape()

    assert len(jobs) > 0

    first_job = jobs[0]

    assert first_job.title
    assert first_job.company_name
    assert first_job.source_name == "adzuna"
    assert first_job.source_url

    print(f"Collected jobs: {len(jobs)}")
    print(f"First job: {first_job.title}")