from collections import Counter

from sqlalchemy import select

from src.analytics.job_relevance import is_data_ai_job
from src.database.connection import get_db_session
from src.database.models.job import Job
from src.database.models.job_skill import JobSkill
from src.database.models.skill import Skill


def main():
    with get_db_session() as session:
        jobs = session.execute(
            select(
                Job.id,
                Job.title,
                Job.location,
            ).where(
                Job.source_name != "manual-test"
            )
        ).all()

        skill_rows = session.execute(
            select(
                JobSkill.job_id,
                Skill.name,
            ).join(
                Skill,
                JobSkill.skill_id == Skill.id,
            )
        ).all()

        skills_by_job: dict[int, set[str]] = {}

        for job_id, skill_name in skill_rows:
            skills_by_job.setdefault(job_id, set()).add(skill_name)

        location_counter = Counter()

        for job_id, title, location in jobs:
            skills = skills_by_job.get(job_id, set())

            if is_data_ai_job(title, skills):
                normalized_location = (
                    location.strip()
                    if location
                    else "Unknown"
                )

                location_counter[normalized_location] += 1

        print("Top Data/AI Locations:")

        for location, count in location_counter.most_common(15):
            print(f"{location}: {count}")


if __name__ == "__main__":
    main()