from src.analytics.data_ai_roles import classify_data_ai_role


def test_classifies_data_ai_roles():
    assert classify_data_ai_role("Senior Data Analyst") == "Data Analyst"
    assert classify_data_ai_role("Junior Data Scientist") == "Data Scientist"
    assert classify_data_ai_role("Lead Data Engineer") == "Data Engineer"
    assert (
        classify_data_ai_role("Senior Machine Learning Engineer")
        == "Machine Learning Engineer"
    )
    assert classify_data_ai_role("Junior AI Engineer") == "AI Engineer"
    assert (
        classify_data_ai_role("Business Intelligence Analyst")
        == "Business Intelligence"
    )


def test_ignores_unrelated_roles():
    assert classify_data_ai_role("Software Engineer") is None
    assert classify_data_ai_role("Product Manager") is None
    assert classify_data_ai_role(None) is None