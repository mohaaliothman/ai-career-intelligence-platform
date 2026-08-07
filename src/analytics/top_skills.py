from sqlalchemy import desc, func, select

from src.database.connection import get_db_session
from src.database.models.job_skill import JobSkill
from src.database.models.skill import Skill


def get_top_skills(limit: int = 10):
    with get_db_session() as session:
        statement = (
            select(
                Skill.name,
                func.count(JobSkill.job_id).label("job_count"),
            )
            .join(JobSkill, Skill.id == JobSkill.skill_id)
            .group_by(Skill.id, Skill.name)
            .order_by(desc("job_count"))
            .limit(limit)
        )

        return session.execute(statement).all()


if __name__ == "__main__":
    results = get_top_skills()

    for skill_name, job_count in results:
        print(f"{skill_name}: {job_count}")