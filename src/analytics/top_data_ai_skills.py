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

        skill_counter = Counter()
        data_ai_jobs = 0
        data_ai_jobs_with_skills = 0

        for job_id, title in jobs:
            skills = skills_by_job.get(job_id, set())

            if is_data_ai_job(title, skills):
                data_ai_jobs += 1

                if skills:
                    data_ai_jobs_with_skills += 1
                    skill_counter.update(skills)

        data_ai_jobs_without_skills = (
            data_ai_jobs - data_ai_jobs_with_skills
        )

        print(f"Total Data/AI Jobs: {data_ai_jobs}")
        print(
            f"Data/AI Jobs with Skills: "
            f"{data_ai_jobs_with_skills}"
        )
        print(
            f"Data/AI Jobs without Skills: "
            f"{data_ai_jobs_without_skills}"
        )

        print("\nTop Data/AI Skills:")

        for skill, count in skill_counter.most_common(15):
            print(f"{skill}: {count}")



if __name__ == "__main__":
    main()