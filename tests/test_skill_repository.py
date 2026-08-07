from src.database.connection import get_db_session
from src.database.repositories.skill_repository import SkillRepository


def test_get_or_create_skill():
    with get_db_session() as session:
        repository = SkillRepository(session)

        first_skill = repository.get_or_create("Python")
        second_skill = repository.get_or_create("Python")

        print("First ID:", first_skill.id)
        print("Second ID:", second_skill.id)
        print("Skill name:", second_skill.name)

        assert first_skill.id == second_skill.id
        assert second_skill.name == "Python"