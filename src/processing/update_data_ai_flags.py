from sqlalchemy import select

from src.analytics.job_relevance import is_data_ai_job
from src.database.connection import get_db_session
from src.database.models.job import Job
from src.database.models.job_skill import JobSkill
from src.database.models.skill import Skill
from src.analytics.data_ai_roles import classify_data_ai_role


def main():
    with get_db_session() as session:
        jobs = session.execute(
            select(Job)
        ).scalars().all()

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

        data_ai_count = 0

        for job in jobs:
            skills = skills_by_job.get(job.id, set())

            job.is_data_ai = is_data_ai_job(
                job.title,
                skills,
            )

            job.data_ai_role = (
                classify_data_ai_role(job.title)
                if job.is_data_ai
                else None
            )


            if job.is_data_ai:
                data_ai_count += 1

        session.commit()

        print(f"Updated jobs: {len(jobs)}")
        print(f"Data/AI jobs: {data_ai_count}")


if __name__ == "__main__":
    main()