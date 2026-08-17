from collections import Counter

from sqlalchemy import select

from src.database.connection import get_db_session
from src.database.models.job import Job


ROLE_PATTERNS = {
    "Data Analyst": [
        "data analyst",
    ],
    "Data Scientist": [
        "data scientist",
        "data science",
    ],
    "Data Engineer": [
        "data engineer",
        "data engineering",
    ],
    "Machine Learning Engineer": [
        "machine learning engineer",
        "ml engineer",
        "mle",
    ],
    "AI Engineer": [
        "ai engineer",
        "artificial intelligence engineer",
    ],
    "Business Intelligence": [
        "business intelligence",
        "bi analyst",
        "bi developer",
    ],
}


def classify_data_ai_role(title: str | None) -> str | None:
    if not title:
        return None

    normalized_title = title.lower().strip()

    for role, patterns in ROLE_PATTERNS.items():
        if any(pattern in normalized_title for pattern in patterns):
            return role

    return None



def main():
    role_counter = Counter()

    with get_db_session() as session:
        jobs = session.execute(
            select(Job.title).where(
                Job.source_name != "manual-test"
            )
        ).scalars().all()

        for title in jobs:
            role = classify_data_ai_role(title)

            if role:
                role_counter[role] += 1

    print("Data/AI Roles:")

    for role, count in role_counter.most_common():
        print(f"{role}: {count}")


if __name__ == "__main__":
    main()