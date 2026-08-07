from sqlalchemy import select

from src.database.connection import get_db_session
from src.database.models.job import Job
from src.database.models.job_skill import JobSkill
from src.database.models.skill import Skill
from src.processing.job_skill_processor import process_job_skills


def test_process_job_skills():
    with get_db_session() as session:
        job = session.scalar(
            select(Job).where(Job.id == 6)
        )

        assert job is not None

        job.description = """
        We are looking for an AI Engineer with experience in
        Python, SQL, machine learning, Docker, and AWS.
        """

        extracted_skills = process_job_skills(job, session)

        print("Extracted skills:", extracted_skills)

        assert "python" in extracted_skills
        assert "sql" in extracted_skills
        assert "machine learning" in extracted_skills
        assert "docker" in extracted_skills
        assert "aws" in extracted_skills

        relations = session.scalars(
            select(JobSkill).where(JobSkill.job_id == job.id)
        ).all()

        skill_ids = [relation.skill_id for relation in relations]

        skills = session.scalars(
            select(Skill).where(Skill.id.in_(skill_ids))
        ).all()

        stored_skill_names = {skill.name for skill in skills}

        print("Stored skills:", stored_skill_names)

        assert extracted_skills.issubset(stored_skill_names)