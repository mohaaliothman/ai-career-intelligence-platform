import re


SKILL_ALIASES = {
    "python": {"python"},
    "sql": {"sql"},
    "postgresql": {"postgresql", "postgres"},
    "mysql": {"mysql"},
    "sql server": {"sql server", "mssql"},
    "oracle": {"oracle", "pl/sql", "plsql"},
    "excel": {"excel", "microsoft excel"},
    "power bi": {"power bi", "powerbi"},
    "tableau": {"tableau"},
    "pandas": {"pandas"},
    "numpy": {"numpy"},
    "scikit-learn": {"scikit-learn", "sklearn"},
    "machine learning": {"machine learning"},
    "deep learning": {"deep learning"},
    "natural language processing": {
        "natural language processing",
        "nlp",
    },
    "computer vision": {"computer vision"},
    "statistics": {"statistics", "statistical analysis"},
    "data visualization": {
        "data visualization",
        "data visualisation",
    },
    "data analysis": {"data analysis", "data analytics"},
    "data engineering": {"data engineering"},
    "etl": {"etl", "extract transform load"},
    "airflow": {"airflow", "apache airflow"},
    "spark": {"spark", "apache spark", "pyspark"},
    "aws": {"aws", "amazon web services"},
    "azure": {"azure", "microsoft azure"},
    "google cloud": {"google cloud", "gcp"},
    "docker": {"docker"},
    "git": {"git", "github"},
}


def extract_skills(text: str | None) -> set[str]:
    """
    Extract normalized technical skills from job text.
    """
    if not text:
        return set()

    normalized_text = text.lower()
    extracted_skills: set[str] = set()

    for normalized_skill, aliases in SKILL_ALIASES.items():
        if any(_contains_alias(normalized_text, alias) for alias in aliases):
            extracted_skills.add(normalized_skill)

    return extracted_skills


def _contains_alias(text: str, alias: str) -> bool:
    """
    Check whether an alias exists as a complete term.
    """
    pattern = rf"(?<!\w){re.escape(alias.lower())}(?!\w)"
    return re.search(pattern, text) is not None