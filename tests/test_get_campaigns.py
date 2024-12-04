from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_campaigns_response_structure():
    response = client.get("/api/v1/campaigns")
    data = response.json()
    
    if len(data) > 0:  # Only test structure if there are campaigns
        campaign = data[0]
        assert "campaign_id" in campaign
        assert "campaign_name" in campaign
        assert "campaign_type" in campaign
        assert "num_ad_groups" in campaign
        assert "ad_group_names" in campaign
        assert "avg_monthly_cost" in campaign
        assert "avg_cost_per_conversion" in campaign
        
        assert isinstance(campaign["campaign_id"], int)
        assert isinstance(campaign["campaign_name"], str)
        assert isinstance(campaign["campaign_type"], str)
        assert isinstance(campaign["num_ad_groups"], int)
        assert isinstance(campaign["ad_group_names"], list)
        assert isinstance(campaign["avg_monthly_cost"], float)
        assert isinstance(campaign["avg_cost_per_conversion"], float)


