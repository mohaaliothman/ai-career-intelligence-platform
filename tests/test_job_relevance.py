from src.analytics.job_relevance import is_data_ai_title, has_strong_data_skills, is_data_ai_job


def test_data_ai_titles():
    assert is_data_ai_title("Junior Data Analyst") is True
    assert is_data_ai_title("Senior Data Scientist") is True
    assert is_data_ai_title("BI Analyst") is True
    assert is_data_ai_title("Machine Learning Engineer") is True
    assert is_data_ai_title("Business Intelligence Specialist") is True


def test_non_data_ai_titles():
    assert is_data_ai_title("Software Engineer") is False
    assert is_data_ai_title("Backend Developer") is False
    assert is_data_ai_title("DevOps Engineer") is False
    assert is_data_ai_title("Frontend Developer") is False


def test_missing_title():
    assert is_data_ai_title(None) is False
    assert is_data_ai_title("") is False


def test_strong_data_skills():
    assert has_strong_data_skills({"sql", "power bi"}) is True
    assert has_strong_data_skills({"pandas", "machine learning"}) is True
    assert has_strong_data_skills({"data analysis", "excel", "sql"}) is True


def test_general_technical_skills_are_not_enough():
    assert has_strong_data_skills({"python", "git", "docker", "aws"}) is False
    assert has_strong_data_skills({"python", "sql"}) is False
    assert has_strong_data_skills({"docker", "azure"}) is False


def test_single_core_data_skill_is_not_enough():
    assert has_strong_data_skills({"sql"}) is False
    assert has_strong_data_skills({"machine learning"}) is False


def test_empty_skills():
    assert has_strong_data_skills(set()) is False


def test_is_data_ai_job():
    assert is_data_ai_job(
        "Junior Data Analyst",
        {"excel"},
    ) is True

    assert is_data_ai_job(
        "Reporting Specialist",
        {"sql", "power bi", "excel"},
    ) is True

    assert is_data_ai_job(
        "Software Engineer",
        {"python", "docker", "aws"},
    ) is False