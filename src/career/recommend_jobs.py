from sqlalchemy import select

from src.analytics.job_relevance import is_data_ai_job
from src.career.feature_builder import build_job_text
from src.career.job_matcher import calculate_job_matches
from src.database.connection import get_db_session
from src.database.models.job import Job
from src.database.models.job_skill import JobSkill
from src.database.models.skill import Skill


def recommend_jobs(
    user_skills: str,
    limit: int = 5,
) -> list[dict]:
    with get_db_session() as session:
        jobs = session.execute(
            select(
                Job.id,
                Job.title,
                Job.company_name,
                Job.location,
                Job.description,
                Job.source_url,
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

        candidate_jobs = []
        job_texts = []

        for job in jobs:
            skills = skills_by_job.get(job.id, set())

            if not is_data_ai_job(job.title, skills):  #A regular Software Engineer won't compete with a Data Analyst just because he has Python.
                continue

            job_text = build_job_text(
                title=job.title,
                skills=skills,
                description=job.description,
            )

            candidate_jobs.append(
                {
                    "title": job.title,
                    "company": job.company_name,
                    "location": job.location,
                    "url": job.source_url,
                }
            )

            job_texts.append(job_text)

        scores = calculate_job_matches(
            user_text=user_skills,
            job_texts=job_texts,
        )

        for job, score in zip(candidate_jobs, scores):
            job["score"] = score

        ranked_jobs = sorted(  ## It ranks jobs from highest similarity to lowest.
            candidate_jobs,
            key=lambda job: job["score"],
            reverse=True,
        )

        unique_jobs = []
        seen_jobs = set()

        for job in ranked_jobs:
            job_key = (
                job["company"].lower().strip(),
                job["title"].lower().strip(),
            )

            if job_key in seen_jobs:
                continue

            seen_jobs.add(job_key)
            unique_jobs.append(job)

            if len(unique_jobs) == limit:
                break

        return unique_jobs


def main():
    user_skills = input(
        "Enter your skills (example: python sql excel power bi): "
    )

    recommendations = recommend_jobs(user_skills)

    print("\nTop Recommended Jobs:\n")

    for index, job in enumerate(recommendations, start=1):
        print(
            f"{index}. {job['title']} | "
            f"{job['company']} | "
            f"{job['location']} | "
            f"Match: {job['score']:.1%}"
        )


if __name__ == "__main__":
    main()