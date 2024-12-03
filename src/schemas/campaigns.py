from pydantic import BaseModel
from typing import List

class CampaignMetrics(BaseModel):
    campaign_id: int
    campaign_name: str
    campaign_type: str
    num_ad_groups: int
    ad_group_names: List[str]
    avg_monthly_cost: float
    avg_cost_per_conversion: float

