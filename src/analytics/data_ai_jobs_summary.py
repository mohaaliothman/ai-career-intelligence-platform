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
                Job.description,
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

        total_jobs = len(jobs)
        data_ai_jobs = 0
        over_1000 = 0
        over_2000 = 0

        for job_id, title, description in jobs:
            skills = skills_by_job.get(job_id, set())

            if is_data_ai_job(title, skills):
                data_ai_jobs += 1

                description_length = len(description or "")

                if description_length >= 1000:
                    over_1000 += 1

                if description_length >= 2000:
                    over_2000 += 1

        non_data_ai_jobs = total_jobs - data_ai_jobs

        print(f"Total Jobs: {total_jobs}")
        print(f"Data/AI Jobs: {data_ai_jobs}")
        print(f"Non-Data/AI Jobs: {non_data_ai_jobs}")
        print(f"Description >= 1000: {over_1000}")
        print(f"Description >= 2000: {over_2000}")


if __name__ == "__main__":
    main()