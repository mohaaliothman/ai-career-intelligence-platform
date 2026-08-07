from datetime import datetime

import requests

from src.scraper.base_scraper import BaseScraper
from src.scraper.models import ScrapedJob


class JobicyScraper(BaseScraper):
    BASE_URL = "https://jobicy.com/api/v2/remote-jobs"

    def scrape(self) -> list[ScrapedJob]:
        response = requests.get(
            self.BASE_URL,
            params={"count": 50},
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for item in data.get("jobs", []):
            job = ScrapedJob(
                title=item["jobTitle"],
                company_name=item["companyName"],
                location=item.get("jobGeo"),
                employment_type=self._first(item.get("jobType")),
                experience_level=item.get("jobLevel"),
                description=item.get("jobDescription"),
                source_name="jobicy",
                source_url=item["url"],
                posted_at=self._parse_date(item.get("pubDate")),
            )

            jobs.append(job)

        return jobs

    @staticmethod
    def _first(value: list | None) -> str | None:
        if not value:
            return None

        return value[0]

    @staticmethod
    def _parse_date(value: str | None) -> datetime | None:
        if not value:
            return None

        return datetime.fromisoformat(value)