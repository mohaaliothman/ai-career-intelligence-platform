"""Base functionality shared by all job scrapers """

from abc import ABC, abstractmethod

import requests
from requests import Response

from src.scraper.models import ScrapedJob

class BaseScraper(ABC): # we use ABC So that we don't create BaseScraper directly, but rather use it as the basis for any website
    """Provide shared HTTP behavior for job scrapers """

    def __init__(self, timeout: int = 20) -> None :
        self.timeout = timeout
        self.headers = {
            "User-Agent":(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/150.0.0.0 Safari/537.36"
            )
        }

    def _get(self, url: str) -> Response:
        """Send a GET request and return a successful response """

        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.timeout,
        )

        response.raise_for_status() #So that errors such as 404 and 500 become clear exceptions instead of continuing execution with a failed page

        return response
    
    @abstractmethod
    def scrape(self) -> list[ScrapedJob]:
        """Collect and return jibs from the external source """

        raise NotImplementedError