import os
from datetime import datetime
from decimal import Decimal

import requests
from dotenv import load_dotenv

from src.scraper.base_scraper import BaseScraper
from src.scraper.models import ScrapedJob


load_dotenv()


class AdzunaScraper(BaseScraper):
    BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/1"  ## The same function cannot be added more than once if it appears under more than one search term.

    SEARCH_TERMS = [  ## The source is targeted for Data/AI
        "data analyst",
        "data scientist",
        "data engineer",
        "business intelligence",
        "machine learning engineer",
        "ai engineer",
    ]

    def scrape(self) -> list[ScrapedJob]:
        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")

        if not app_id or not app_key:
            raise ValueError("Missing Adzuna API credentials")

        jobs: list[ScrapedJob] = []
        seen_urls: set[str] = set()

        for search_term in self.SEARCH_TERMS:
            params = {
                "app_id": app_id,
                "app_key": app_key,
                "what": search_term,
                "results_per_page": 20,
            }

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=15,
            )

            response.raise_for_status()  ## It makes any API problem appear immediately instead of us failing silently.

            data = response.json()

            for item in data.get("results", []):
                source_url = item.get("redirect_url")

                if not source_url or source_url in seen_urls:
                    continue

                seen_urls.add(source_url)

                jobs.append(
                    ScrapedJob(
                        title=item.get("title", "").strip(),
                        company_name=(
                            item.get("company", {}).get("display_name")
                            or "Unknown"
                        ),
                        location=(
                            item.get("location", {}).get("display_name")
                        ),
                        description=item.get("description"),
                        salary_min=self._to_decimal(
                            item.get("salary_min")
                        ),
                        salary_max=self._to_decimal(
                            item.get("salary_max")
                        ),
                        salary_currency="GBP",
                        source_name="adzuna",
                        source_url=source_url,
                        posted_at=self._parse_datetime(
                            item.get("created")
                        ),
                        scraped_at=datetime.now().astimezone(),
                    )
                )

        return jobs

    @staticmethod
    def _to_decimal(value) -> Decimal | None:
        if value is None:
            return None

        return Decimal(str(value))

    @staticmethod
    def _parse_datetime(value: str | None):
        if not value:
            return None

        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )