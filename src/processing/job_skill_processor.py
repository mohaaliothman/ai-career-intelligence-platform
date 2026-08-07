from sqlalchemy.orm import Session

from src.database.models.job import Job
from src.database.repositories.job_skill_repository import JobSkillRepository
from src.database.repositories.skill_repository import SkillRepository
from src.processing.skills_extractor import extract_skills


def process_job_skills(job: Job, session: Session) -> set[str]:
    text = f"{job.title or ''}{job.description or ''}"

    extracted_skills = extract_skills(text)

    skill_repository = SkillRepository(session)
    job_skill_repository = JobSkillRepository(session)

    for skill_name in extracted_skills:
        skill = skill_repository.get_or_create(skill_name)

        job_skill_repository.create(
            job_id=job.id,
            skill_id=skill.id,
        )

    return extracted_skills