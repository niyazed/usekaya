from src.services.campaigns import _calculate_campaign_metrics

def test_calculate_campaign_metrics():
    # Create mock campaign data
    class MockStats:
        def __init__(self, cost, conversions):
            self.cost = cost
            self.conversions = conversions
            
    class MockAdGroup:
        def __init__(self, stats):
            self.ad_group_stats = stats
            
    class MockCampaign:
        def __init__(self, ad_groups):
            self.ad_groups = ad_groups

    # Test case 1: Campaign with multiple ad groups and stats
    stats1 = [MockStats(100.50, 10), MockStats(200.25, 20)]
    stats2 = [MockStats(150.75, 15), MockStats(300.00, 25)]
    ad_groups = [
        MockAdGroup(stats1),
        MockAdGroup(stats2)
    ]
    campaign = MockCampaign(ad_groups)
    
    metrics = _calculate_campaign_metrics(campaign)
    
    # Total cost should be 751.50 (100.50 + 200.25 + 150.75 + 300.00)
    # Average monthly cost should be 751.50 / 12 = 62.625
    # Total conversions should be 70 (10 + 20 + 15 + 25)
    # Cost per conversion should be 751.50 / 70 = 10.735714...
    
    assert metrics["avg_monthly_cost"] == 62.63
    assert metrics["cost_per_conversion"] == 10.74
    
    # Test case 2: Campaign with no conversions
    stats_no_conv = [MockStats("100.00", 0)]
    campaign_no_conv = MockCampaign([MockAdGroup(stats_no_conv)])
    
    metrics_no_conv = _calculate_campaign_metrics(campaign_no_conv)
    
    assert round(metrics_no_conv["avg_monthly_cost"], 2) == 8.33  # 100/12
    assert metrics_no_conv["cost_per_conversion"] == 0
    
    # Test case 3: Campaign with no cost
    stats_no_cost = [MockStats("0", 10)]
    campaign_no_cost = MockCampaign([MockAdGroup(stats_no_cost)])
    
    metrics_no_cost = _calculate_campaign_metrics(campaign_no_cost)
    
    assert metrics_no_cost["avg_monthly_cost"] == 0
    assert metrics_no_cost["cost_per_conversion"] == 0