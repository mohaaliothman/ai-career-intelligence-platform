""" why Remotive ?
            Because it provides a public API for functions """

"""Scraper for the Remotive Jobs API """

from src.scraper.base_scraper import BaseScraper
from src.scraper.models import ScrapedJob


class RemotiveScraper(BaseScraper):
    """Collect jobs from the Remotive API """

    API_URL = "https://remotive.com/api/remote-jobs"

    def scrape(self) -> list[ScrapedJob]:
        """Collect and return jobs from Remotive."""

        response = self._get(self.API_URL)
        data = response.json()

        jobs: list[ScrapedJob] = []

        for item in data["jobs"]:
            jobs.append(
                ScrapedJob(
                    title=item.get("title", ""),
                    company_name=item.get("company_name", ""),
                    location=item.get("candidate_required_location"),
                    employment_type=item.get("job_type"),
                    description=item.get("description"),
                    source_name="Remotive",
                    source_url=item.get("url", ""),
                )
            )

        return jobs