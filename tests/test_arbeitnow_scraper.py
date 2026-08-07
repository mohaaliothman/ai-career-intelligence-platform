from src.scraper.sources.arbeitnow_scraper import ArbeitnowScraper


def test_arbeitnow_scraper_collects_jobs():
    scraper = ArbeitnowScraper()

    jobs = scraper.scrape()

    print("Collected jobs:", len(jobs))

    assert len(jobs) > 0

    first_job = jobs[0]

    print("Title:", first_job.title)
    print("Company:", first_job.company_name)
    print("Location:", first_job.location)
    print("Source:", first_job.source_name)
    print("Posted at:", first_job.posted_at)

    assert first_job.title
    assert first_job.company_name
    assert first_job.source_name == "arbeitnow"
    assert first_job.source_url