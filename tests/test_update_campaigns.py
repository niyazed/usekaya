from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_update_campaign():
    params = {"campaign_id": 18301866406, "campaign_name": "Testing"}
    response = client.patch("/api/v1/campaigns", params=params)
    assert response.status_code == 200
    data = response.json()
    assert data["campaign_id"] == 18301866406
        
    # Revert back the changes
    params = {"campaign_id": 18301866406, "campaign_name": "Clothing"}
    response = client.patch("/api/v1/campaigns", params=params)
    
def test_update_campaign_error():
    params = {"campaign_id": 18301866405, "campaign_name": "Testing"}
    response = client.patch("/api/v1/campaigns", params=params)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Campaign with ID {params['campaign_id']} not found"