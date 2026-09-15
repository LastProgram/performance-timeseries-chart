from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_index_serves_chart_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'id="performance-chart"' in response.text


def test_prepare_chart_accepts_four_time_series() -> None:
    response = client.post(
        "/api/chart",
        json={
            "cost": [{"timestamp": "2026-06-12T00:00:00Z", "value": 44.36}],
            "cpa": [{"timestamp": "2026-06-12T00:00:00Z", "value": 1.23}],
            "roi_confirmed": [
                {"timestamp": "2026-06-12T00:00:00Z", "value": 161.47}
            ],
            "conversions": [{"timestamp": "2026-06-12T00:00:00Z", "value": 36}],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["cost"] == [44.36]
    assert payload["cpa"] == [1.23]
    assert payload["roi_confirmed"] == [161.47]
    assert payload["conversions"] == [36.0]


def test_prepare_chart_returns_422_for_duplicate_timestamp() -> None:
    duplicate = {"timestamp": "2026-06-12T00:00:00Z", "value": 10}
    response = client.post(
        "/api/chart",
        json={
            "cost": [duplicate, duplicate],
            "cpa": [],
            "roi_confirmed": [],
            "conversions": [],
        },
    )

    assert response.status_code == 422
    assert "duplicate timestamp" in response.json()["detail"]
