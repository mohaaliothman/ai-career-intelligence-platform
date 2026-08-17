from sqlalchemy import func, select

from src.database.connection import get_db_session
from src.database.models.job import Job


def get_top_companies(limit: int = 10):
    statement = (   
        select(
            Job.company_name,
            func.count(Job.id).label("total_jobs"),   ## It counts all the company's advertisements.
            func.count(func.distinct(Job.title)).label("unique_job_titles"),   ## It counts the number of different job titles.
        )
        .where(Job.company_name.is_not(None))
        .group_by(Job.company_name)
        .order_by(  ##We tell the database: First, rank the companies by job diversity. If two companies have the same diversity, rank them by total number of jobs.
            func.count(func.distinct(Job.title)).desc(),
            func.count(Job.id).desc(),
        )
        .limit(limit)
    )

    with get_db_session() as session:
        return session.execute(statement).all()


def main():
    companies = get_top_companies()

    for company_name, total_jobs, unique_job_titles in companies:
        print(
            f"{company_name}: "
            f"{total_jobs} jobs | "
            f"{unique_job_titles} unique roles"
        )


if __name__ == "__main__":
    main()