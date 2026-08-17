from src.career.feature_builder import build_job_text


def test_build_job_text():
    result = build_job_text(
        title="Data Analyst",
        skills={"SQL", "Excel", "Power BI"},
        description="Analyze business data.",
    )

    assert "data analyst" in result
    assert "sql" in result
    assert "excel" in result
    assert "power bi" in result
    assert "analyze business data" in result


def test_build_job_text_handles_missing_values():
    result = build_job_text(
        title="Data Analyst",
        skills=set(),
        description=None,
    )

    assert result == "data analyst data analyst data analyst"