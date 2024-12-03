from pydantic import BaseModel
from typing import Optional, List
class FilterParams(BaseModel):
    """
    Filter parameters for performance time series data
    """
    model_config = {"extra": "forbid"}
    
    aggregate_by: str
    campaigns: Optional[List[int]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class PerformanceTimeSeries(BaseModel):
    """
    Response schema for performance time series data
    """
    total_cost: float
    total_clicks: int
    total_conversions: int
    avg_cost_per_click: float
    avg_cost_per_conversion: float
    avg_click_through_rate: float
    avg_conversion_rate: float
