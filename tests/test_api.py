from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.main import app, create_app
from app.schemas import PerformanceSeriesInput, TimeSeriesPoint

client = TestClient(app)


def test_index_serves_chart_page() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'id="performance-chart"' in response.text
    assert 'class="today-summary"' in response.text
    assert "Tdy" in response.text
    assert "0%" in response.text
    assert "$0" in response.text
    assert "—" in response.text


def test_demo_chart_matches_reference_values() -> None:
    response = client.get("/api/chart")

    assert response.status_code == 200
    payload = response.json()
    assert payload["cost"] == [2.04, 25.85, 44.35, 55.65, 63.75]
    assert payload["cpa"] == [0.68, 0.86, 1.23, 0.79, 0.71]
    assert payload["roi_confirmed"] == [610.78, 180.5, 161.47, 56.33, 357.25]
    assert payload["conversions"] == [3.0, 30.0, 36.0, 70.0, 90.0]


def test_create_app_uses_supplied_time_series() -> None:
    timestamp = datetime(2026, 6, 12, tzinfo=UTC)
    custom_data = PerformanceSeriesInput(
        cost=[TimeSeriesPoint(timestamp=timestamp, value=10)],
        cpa=[TimeSeriesPoint(timestamp=timestamp, value=2)],
        roi_confirmed=[TimeSeriesPoint(timestamp=timestamp, value=150)],
        conversions=[TimeSeriesPoint(timestamp=timestamp, value=5)],
    )
    custom_client = TestClient(create_app(custom_data))

    response = custom_client.get("/api/chart")

    assert response.status_code == 200
    assert response.json()["cost"] == [10.0]
    assert response.json()["cpa"] == [2.0]
    assert response.json()["roi_confirmed"] == [150.0]
    assert response.json()["conversions"] == [5.0]


def test_prepare_chart_accepts_four_time_series() -> None:
    response = client.post(
        "/api/chart/normalize",
        json={
            "cost": [{"timestamp": "2026-06-12T00:00:00Z", "value": 44.35}],
            "cpa": [{"timestamp": "2026-06-12T00:00:00Z", "value": 1.23}],
            "roi_confirmed": [
                {"timestamp": "2026-06-12T00:00:00Z", "value": 161.47}
            ],
            "conversions": [{"timestamp": "2026-06-12T00:00:00Z", "value": 36}],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["cost"] == [44.35]
    assert payload["cpa"] == [1.23]
    assert payload["roi_confirmed"] == [161.47]
    assert payload["conversions"] == [36.0]


def test_prepare_chart_returns_422_for_duplicate_timestamp() -> None:
    duplicate = {"timestamp": "2026-06-12T00:00:00Z", "value": 10}
    response = client.post(
        "/api/chart/normalize",
        json={
            "cost": [duplicate, duplicate],
            "cpa": [],
            "roi_confirmed": [],
            "conversions": [],
        },
    )

    assert response.status_code == 422
    assert "duplicate timestamp" in response.json()["detail"]
