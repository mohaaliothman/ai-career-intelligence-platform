from src.processing.skills_extractor import extract_skills


def test_extracts_multiple_skills() -> None:
    text = """
    We are looking for a Data Analyst with experience
    in Python, SQL, Power BI and Microsoft Excel.
    """

    result = extract_skills(text)

    assert result == {"python", "sql", "power bi", "excel"}


def test_normalizes_skill_aliases() -> None:
    text = "Experience with Postgres, PowerBI and sklearn is required."

    result = extract_skills(text)

    assert result == {"postgresql", "power bi", "scikit-learn"}


def test_ignores_duplicate_skills() -> None:
    text = "Python experience is required. Strong Python knowledge is preferred."

    result = extract_skills(text)

    assert result == {"python"}


def test_returns_empty_set_for_unrelated_text() -> None:
    text = "The candidate should have excellent communication skills."

    result = extract_skills(text)

    assert result == set()


def test_handles_missing_text() -> None:
    result = extract_skills(None)

    assert result == set()


def test_does_not_match_partial_words() -> None:
    text = "The company uses GitLab for collaboration."

    result = extract_skills(text)

    assert "git" not in result