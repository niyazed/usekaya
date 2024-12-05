from .conftest import client

def test_get_performance_time_series(client):
    params = {"aggregate_by": "day"}
    response = client.get("/api/v1/performance-time-series", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
