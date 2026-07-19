""" Data models used by the scraper layer """

from dataclasses import dataclass 
from datetime import datetime
from decimal import Decimal 

@dataclass(slots=True)  #It reduces the writing of code (we don't write __init__ manually).
class ScrapedJob:
    """ Represents a job collected from an external source """

    title: str
    company_name: str

    location: str | None= None
    employment_type: str | None= None
    experience_level: str | None= None

    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    salary_currency: str | None = None

    description: str | None = None

    source_name: str = ""
    source_url: str = ""

    posted_at: datetime | None = None
    scraped_at: datetime | None = None