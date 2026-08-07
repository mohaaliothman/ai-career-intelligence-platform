from sqlalchemy import select

from src.database.connection import get_db_session
from src.database.models.job import Job
from src.processing.job_skill_processor import process_job_skills


def process_all_job_skills() -> None:
    with get_db_session() as session:
        jobs = session.scalars(
            select(Job).where(Job.is_active.is_(True))
        ).all()

        processed_jobs = 0
        total_skills = 0

        for job in jobs:
            extracted_skills = process_job_skills(job, session)

            processed_jobs += 1
            total_skills += len(extracted_skills)

        print(f"Processed jobs: {processed_jobs}")
        print(f"Extracted skill relations: {total_skills}")


if __name__ == "__main__":
    process_all_job_skills()