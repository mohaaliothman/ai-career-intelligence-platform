from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.job_skill import JobSkill
from src.database.repositories.base_repository import BaseRepository


class JobSkillRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def exists(self, job_id: int, skill_id: int) -> bool:
        statement = select(JobSkill).where(
            JobSkill.job_id == job_id,
            JobSkill.skill_id == skill_id,
        )

        return self._session.scalar(statement) is not None

    def create(self, job_id: int, skill_id: int) -> JobSkill:
        if self.exists(job_id, skill_id):
            return self._session.scalar(
                select(JobSkill).where(
                    JobSkill.job_id == job_id,
                    JobSkill.skill_id == skill_id,
                )
            )

        job_skill = JobSkill(
            job_id=job_id,
            skill_id=skill_id,
        )

        return self._add(job_skill)