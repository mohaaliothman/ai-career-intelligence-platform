from src.scraper.sources.jobicy_scraper import JobicyScraper


def test_jobicy_scraper_collects_jobs():
    scraper = JobicyScraper()

    jobs = scraper.scrape()

    print("Collected jobs:", len(jobs))

    assert len(jobs) > 0

    first_job = jobs[0]

    print("Title:", first_job.title)
    print("Company:", first_job.company_name)
    print("Location:", first_job.location)
    print("Source:", first_job.source_name)

    assert first_job.title
    assert first_job.company_name
    assert first_job.source_name == "jobicy"
    assert first_job.source_url