
DATA_AI_TITLE_KEYWORDS = {  ## Words/labels that give us a strong indication that the job is Data/AI.
    "data analyst",
    "data scientist",
    "data engineer",
    "analytics",
    "business intelligence",
    "bi analyst",
    "machine learning",
    "ml engineer",
    "ai engineer",
    "artificial intelligence",
}

CORE_DATA_SKILLS = {
    "sql",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "statistics",
    "data visualization",
    "data analysis",
    "data engineering",
    "etl",
    "airflow",
    "spark",
}


DATA_RELATED_ROLE_KEYWORDS = {
    "analyst",
    "analytics",
    "reporting",
    "insights",
    "business intelligence",
    "bi ",
}


def is_data_ai_title(title: str | None) -> bool:
    if not title:
        return False

    normalized_title = title.lower().strip()  # because all world treated the same way.

    return any(   # This means if any keyword is found within the title --> True 
        keyword in normalized_title
        for keyword in DATA_AI_TITLE_KEYWORDS
    )


def has_strong_data_skills(skills: set[str]) -> bool:
    normalized_skills = {
        skill.lower().strip()
        for skill in skills
    }

    matched_skills = normalized_skills & CORE_DATA_SKILLS

    return len(matched_skills) >= 2   # why 2 ? Because it reduces false positives. Having SQL alone, for example, might be required in many jobs.


def is_data_ai_job(
    title: str | None,
    skills: set[str],
) -> bool:
    if is_data_ai_title(title):
        return True

    if not title:
        return False

    normalized_title = title.lower().strip()

    has_data_related_role = any(
        keyword in normalized_title
        for keyword in DATA_RELATED_ROLE_KEYWORDS
    )

    return (
        has_data_related_role
        and has_strong_data_skills(skills)
    )
