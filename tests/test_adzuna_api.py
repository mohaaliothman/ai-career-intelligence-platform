import os

import requests
from dotenv import load_dotenv


load_dotenv()


def test_adzuna_api_connection():
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    assert app_id
    assert app_key

    url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": "data analyst",
        "results_per_page": 1,
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    assert response.status_code == 200

    data = response.json()

    assert "results" in data