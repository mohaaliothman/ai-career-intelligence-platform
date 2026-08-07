from datetime import datetime, timezone

import requests

from src.scraper.base_scraper import BaseScraper
from src.scraper.models import ScrapedJob


class ArbeitnowScraper(BaseScraper):
    BASE_URL = "https://www.arbeitnow.com/api/job-board-api"

    def scrape(self) -> list[ScrapedJob]:
        response = requests.get(
            self.BASE_URL,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        jobs = []

        for item in data.get("data", []):
            job = ScrapedJob(
                title=item["title"],
                company_name=item["company_name"],
                location=item.get("location"),
                employment_type=self._first(item.get("job_types")),
                description=item.get("description"),
                source_name="arbeitnow",
                source_url=item["url"],
                posted_at=self._parse_timestamp(item.get("created_at")),
            )

            jobs.append(job)

        return jobs

    @staticmethod
    def _first(value) -> str | None:
        if not value:
            return None

        if isinstance(value, list):
            return value[0]

        if isinstance(value, dict):
            return next(iter(value.values()), None)

        return str(value)

    @staticmethod
    def _parse_timestamp(value: int | None) -> datetime | None:
        if value is None:
            return None

        return datetime.fromtimestamp(
            value,
            tz=timezone.utc,
        )