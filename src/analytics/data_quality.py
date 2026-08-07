from sqlalchemy import func, select

from src.database.connection import get_db_session
from src.database.models.job import Job
from src.database.models.job_skill import JobSkill


def get_data_quality_summary() -> None:
    with get_db_session() as session:
        total_jobs = session.scalar(
            select(func.count(Job.id))
        )

        jobs_without_description = session.scalar(
            select(func.count(Job.id)).where(
                Job.description.is_(None)
            )
        )

        jobs_without_location = session.scalar(
            select(func.count(Job.id)).where(
                Job.location.is_(None)
            )
        )

        total_skill_relations = session.scalar(
            select(func.count()).select_from(JobSkill)
        )

        source_counts = session.execute(
            select(
                Job.source_name,
                func.count(Job.id),
            )
            .group_by(Job.source_name)
            .order_by(func.count(Job.id).desc())
        ).all()

        print("Total jobs:", total_jobs)
        print("Jobs without description:", jobs_without_description)
        print("Jobs without location:", jobs_without_location)
        print("Skill relations:", total_skill_relations)

        print("\nJobs by source:")

        for source_name, count in source_counts:
            print(f"{source_name}: {count}")

if __name__ == "__main__":
    get_data_quality_summary()