from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.skill import Skill
from src.database.repositories.base_repository import BaseRepository

class SkillRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def get_by_name(self, name: str) -> Skill | None:
        statement = select(Skill).where(Skill.name == name)

        return self._session.scalar(statement)

    def get_or_create(
        self,
        name: str,
        category: str | None = None,
    ) -> Skill:
        skill = self.get_by_name(name)

        if skill:
            return skill

        skill = Skill(
            name=name,
            category=category,
        )

        return self._add(skill)