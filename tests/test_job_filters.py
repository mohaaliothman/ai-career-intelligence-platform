from src.processing.filters import contains_ai_data_keyword


def test_matches_keyword_in_title() -> None:
    result = contains_ai_data_keyword(
        title="Senior Data Analyst",
        description="Build reports for the business.",
    )

    assert result is True


def test_matches_keyword_in_description() -> None:
    result = contains_ai_data_keyword(
        title="Python Developer",
        description="Build machine learning pipelines for production.",
    )

    assert result is True


def test_rejects_unrelated_job() -> None:
    result = contains_ai_data_keyword(
        title="Graphic Designer",
        description="Create visual assets for marketing campaigns.",
    )

    assert result is False


def test_handles_missing_description() -> None:
    result = contains_ai_data_keyword(
        title="Data Scientist",
        description=None,
    )

    assert result is True


def test_is_case_insensitive() -> None:
    result = contains_ai_data_keyword(
        title="MACHINE LEARNING ENGINEER",
        description="",
    )

    assert result is True