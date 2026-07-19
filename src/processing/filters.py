from collections.abc import Iterable


AI_DATA_KEYWORDS = {
    # General data roles
    "data analyst",
    "data scientist",
    "data science",
    "data engineer",
    "data engineering",
    "data architect",
    "data analytics",
    "analytics engineer",

    # Artificial intelligence and machine learning
    "artificial intelligence",
    "machine learning",
    "machine learning engineer",
    "ml engineer",
    "ai engineer",
    "ai developer",
    "deep learning",
    "computer vision",
    "natural language processing",
    "nlp engineer",

    # Business intelligence and reporting
    "business intelligence",
    "bi analyst",
    "bi developer",
    "power bi",
    "tableau developer",
    "reporting analyst",

    # Database and analytics-related roles
    "database developer",
    "sql developer",
    "big data",
    "etl developer",
}


def contains_ai_data_keyword(
    title: str | None,
    description: str | None,
    keywords: Iterable[str] = AI_DATA_KEYWORDS,
) -> bool:
    """
    Return True when the job title or description contains
    at least one AI or data-related keyword.
    """
    searchable_text = f"{title or ''} {description or ''}".lower()

    return any(keyword.lower() in searchable_text for keyword in keywords)