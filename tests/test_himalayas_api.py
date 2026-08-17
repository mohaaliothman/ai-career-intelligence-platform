import requests


def test_himalayas_search_results():
    url = "https://himalayas.app/jobs/api"

    params = {
        "q": "data engineer",
        "limit": 20,
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    jobs = response.json().get("jobs", [])

    assert len(jobs) > 0

    print("\nRESULT TITLES:")

    for job in jobs:
        print("-", job.get("title"))