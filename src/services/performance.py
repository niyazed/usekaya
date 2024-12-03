from typing import Dict, List, Optional
from datetime import date
from sqlmodel import Session

from sqlalchemy import func, text
from src.db.models import AdGroupStatsModel, AdGroupModel, CampaignModel

def get_performance_time_series(
    session: Session,
    aggregate_by: str,
    campaigns: Optional[List[int]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict:
    """
    Retrieves performance time series data aggregated by day, week, or month.

    Args:
        session (Session): SQLModel database session
        aggregate_by (str): Time period to aggregate by - must be 'day', 'week', or 'month'
        campaigns (Optional[List[int]], optional): List of campaign IDs to filter by. Defaults to None.
        start_date (Optional[str], optional): Start date for filtering in YYYY-MM-DD format. Defaults to None.
        end_date (Optional[str], optional): End date for filtering in YYYY-MM-DD format. Defaults to None.

    Returns:
        Dict: Dictionary containing aggregated performance metrics including:
            - total_cost: Total spend
            - total_clicks: Total number of clicks
            - total_conversions: Total number of conversions  
            - avg_cost_per_click: Average cost per click
            - avg_cost_per_conversion: Average cost per conversion
            - avg_click_through_rate: Average CTR
            - avg_conversion_rate: Average conversion rate
    """
    
    
    # Build base query
    query = (
        session.query(
            func.sum(AdGroupStatsModel.cost).label('total_cost'),
            func.sum(AdGroupStatsModel.clicks).label('total_clicks'), 
            func.sum(AdGroupStatsModel.conversions).label('total_conversions'),
            func.sum(AdGroupStatsModel.impressions).label('total_impressions')
        )
        .join(AdGroupModel)
        .join(CampaignModel)
    )

    # Apply filters
    if campaigns:
        query = query.filter(CampaignModel.campaign_id.in_(campaigns))
    if start_date:
        query = query.filter(AdGroupStatsModel.date >= start_date)
    if end_date:
        query = query.filter(AdGroupStatsModel.date <= end_date)

    # Add date grouping based on aggregate_by parameter
    date_format = {
        'day': 'YYYY-MM-DD',
        'week': 'YYYY-WW', 
        'month': 'YYYY-MM'
    }
    
    query = query.group_by(func.to_char(text('date::date'), date_format[aggregate_by]))

    # Execute query and calculate metrics
    results = query.all()
    
    metrics = []
    for row in results:
        total_cost = float(row.total_cost) if row.total_cost else 0
        total_clicks = row.total_clicks if row.total_clicks else 0
        total_conversions = row.total_conversions if row.total_conversions else 0
        total_impressions = row.total_impressions if row.total_impressions else 0
        
        # Calculate averages, handling division by zero
        avg_cpc = total_cost / total_clicks if total_clicks > 0 else 0
        avg_cpa = total_cost / total_conversions if total_conversions > 0 else 0
        ctr = total_clicks / total_impressions if total_impressions > 0 else 0
        conv_rate = total_conversions / total_clicks if total_clicks > 0 else 0
        
        metrics.append({
            'total_cost': total_cost,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'avg_cost_per_click': avg_cpc,
            'avg_cost_per_conversion': avg_cpa,
            'avg_click_through_rate': ctr,
            'avg_conversion_rate': conv_rate
        })
        
    
    return metrics
