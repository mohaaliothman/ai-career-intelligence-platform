from src.career.job_matcher import calculate_job_matches


def test_relevant_job_gets_higher_score():
    user_text = "python sql excel power bi"

    job_texts = [
        "data analyst sql excel power bi",
        "frontend developer javascript react css",
    ]

    scores = calculate_job_matches(
        user_text,
        job_texts,
    )

    assert len(scores) == 2
    assert scores[0] > scores[1]


def test_empty_job_list():
    scores = calculate_job_matches(
        "python sql",
        [],
    )

    assert scores == []


def test_empty_user_profile():
    scores = calculate_job_matches(
        "",
        [
            "data analyst sql excel",
            "data scientist python machine learning",
        ],
    )

    assert scores == [0.0, 0.0]