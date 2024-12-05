from .conftest import client


def test_get_compare_performance(client):
    params = {"start_date": "2024-09-15", "end_date": "2024-09-17", "compare_mode": "preceding"}
    response = client.get("/api/v1/compare-performance", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["comparison_period"]["start_date"] == "2024-09-12"
    assert data["comparison_period"]["end_date"] == "2024-09-14"

