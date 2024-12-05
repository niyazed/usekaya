from .conftest import client

def test_update_campaign(client):
    params = {"campaign_id": 18301866406, "campaign_name": "Testing"}
    response = client.patch("/api/v1/campaigns", params=params)
    assert response.status_code == 200
    data = response.json()
    assert data["campaign_id"] == 18301866406
        
    # Revert back the changes
    params = {"campaign_id": 18301866406, "campaign_name": "Clothing"}
    response = client.patch("/api/v1/campaigns", params=params)
    
def test_update_campaign_error(client):
    params = {"campaign_id": 18301866405, "campaign_name": "Testing"}
    response = client.patch("/api/v1/campaigns", params=params)
    assert response.status_code == 404
    assert response.json()["detail"] == f"Campaign with ID {params['campaign_id']} not found"