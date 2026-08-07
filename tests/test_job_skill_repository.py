from src.database.connection import get_db_session
from src.database.repositories.job_repository import JobRepository
from src.database.repositories.skill_repository import SkillRepository
from src.database.repositories.job_skill_repository import JobSkillRepository


def test_create_job_skill_relation():
    with get_db_session() as session:
        job_repository = JobRepository(session)
        skill_repository = SkillRepository(session)
        job_skill_repository = JobSkillRepository(session)

        job = job_repository.get_by_source_url(
            "https://example.com/jobs/context-manager-test"
        )

        assert job is not None

        skill = skill_repository.get_or_create("Python")

        first_relation = job_skill_repository.create(
            job_id=job.id,
            skill_id=skill.id,
        )

        second_relation = job_skill_repository.create(
            job_id=job.id,
            skill_id=skill.id,
        )

        print("Job ID:", first_relation.job_id)
        print("Skill ID:", first_relation.skill_id)

        assert first_relation.job_id == job.id
        assert first_relation.skill_id == skill.id

        assert second_relation.job_id == first_relation.job_id
        assert second_relation.skill_id == first_relation.skill_id