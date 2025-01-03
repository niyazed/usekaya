from src.db.models import CampaignModel
from sqlmodel import Session, select
from typing import Dict
from src.utils.logger import logger

# Main public functions
def get_campaign_metrics(session: Session):
    """
    Return all campaigns and their metrics
    """
    logger.info("Getting campaign metrics")
    campaigns = session.exec(select(CampaignModel)).all()
    return [_get_campaign_data(campaign) for campaign in campaigns]


def update_campaign_name(campaign_id: int, campaign_name: str, session: Session):
    """
    Update the name of a campaign
    """
    logger.info(f"Updating campaign name to {campaign_name} for campaign ID {campaign_id}")
    campaign = session.query(CampaignModel).filter(CampaignModel.campaign_id == campaign_id).first()
    if not campaign:
        raise ValueError(f"Campaign with ID {campaign_id} not found")
    campaign.campaign_name = campaign_name
    session.commit()
    logger.info(f"Campaign name updated to {campaign_name} for campaign ID {campaign_id}")
    return {"message": "Campaign updated successfully", "campaign_id": campaign_id}


# Private helper functions
def _get_campaign_data(campaign) -> Dict:
    """
    Return campaign data including metrics
    """
    logger.info(f"Calculating campaign metrics for campaign ID {campaign.campaign_id}")
    metrics = _calculate_campaign_metrics(campaign)
    return {
        "campaign_id": campaign.campaign_id,
        "campaign_name": campaign.campaign_name,
        "campaign_type": campaign.campaign_type,
        "num_ad_groups": len(campaign.ad_groups),
        "ad_group_names": [group.ad_group_name for group in campaign.ad_groups],
        "avg_monthly_cost": metrics["avg_monthly_cost"],
        "avg_cost_per_conversion": metrics["cost_per_conversion"]
    }


def _calculate_campaign_metrics(campaign) -> Dict:
    """
    Calculate average monthly cost and cost per conversion metrics for a campaign
    
    Args:
        campaign: Campaign model instance containing ad groups and their stats
        
    Returns:
        Dict containing:
            avg_monthly_cost (float): Average monthly cost rounded to 2 decimal places
            cost_per_conversion (float): Average cost per conversion rounded to 2 decimal places
    """
    total_cost = 0
    total_conversions = 0
    
    for ad_group in campaign.ad_groups:
        for stats in ad_group.ad_group_stats:
            total_cost += float(stats.cost)
            total_conversions += stats.conversions
            
    avg_monthly_cost = total_cost / 12 if total_cost > 0 else 0
    cost_per_conversion = total_cost / total_conversions if total_conversions > 0 else 0
    
    logger.info(f"Calculated campaign metrics for campaign ID {campaign.campaign_id}")
    return {
        "avg_monthly_cost": round(avg_monthly_cost, 2),
        "cost_per_conversion": round(cost_per_conversion, 2)
    }



