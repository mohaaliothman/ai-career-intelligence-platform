import requests

from src.analytics.job_relevance import is_data_ai_title


def test_muse_data_ai_relevance():
    url = "https://www.themuse.com/api/public/jobs"

    params = {
        "page": 1,
        "category": "Data and Analytics",
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    jobs = response.json().get("results", [])

    assert len(jobs) > 0

    relevant_jobs = []

    print("\nRESULT TITLES:")

    for job in jobs:
        title = job.get("name")

        is_relevant = is_data_ai_title(title)

        print(
            f"{'[DATA/AI]' if is_relevant else '[OTHER]'} "
            f"{title}"
        )

        if is_relevant:
            relevant_jobs.append(job)

    print(f"\nTotal jobs: {len(jobs)}")
    print(f"Data/AI jobs: {len(relevant_jobs)}")

    assert len(relevant_jobs) > 0