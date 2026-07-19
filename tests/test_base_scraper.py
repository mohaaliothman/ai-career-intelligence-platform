from src.scraper.base_scraper import BaseScraper
from src.scraper.models import ScrapedJob


class TestScraper(BaseScraper):
    def scrape(self) -> list[ScrapedJob]:
        return [
            ScrapedJob(
                title="Data Analyst",
                company_name="Test Company",
                source_name="test",
                source_url="https://example.com/job/1",
            )
        ]


scraper = TestScraper(timeout=10)
jobs = scraper.scrape()

print("Timeout:", scraper.timeout)
print("Jobs count:", len(jobs))
print("First job:", jobs[0].title)