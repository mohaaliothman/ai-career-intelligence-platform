from collections import defaultdict

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
                Job.company_name,
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

        companies = defaultdict(
            lambda: {
                "total_jobs": 0,
                "unique_roles": set(),
            }
        )

        for job_id, title, company_name in jobs:
            skills = skills_by_job.get(job_id, set())

            if is_data_ai_job(title, skills):
                companies[company_name]["total_jobs"] += 1
                companies[company_name]["unique_roles"].add(title)

        ranked_companies = sorted(
            companies.items(),
            key=lambda item: (
                len(item[1]["unique_roles"]),
                item[1]["total_jobs"],
            ),
            reverse=True,
        )

        for company_name, stats in ranked_companies:
            print(
                f"{company_name}: "
                f"{stats['total_jobs']} Data/AI jobs | "
                f"{len(stats['unique_roles'])} unique roles"
            )


if __name__ == "__main__":
    main()