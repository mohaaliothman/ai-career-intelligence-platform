from src.scraper.models import ScrapedJob


job = ScrapedJob(
    title="Data Analyst",
    company_name="OpenAI",
    source_name="manual-test",
    source_url="https://example.com/job/1",
)

print(job)