from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from campaign import CampaignModel
from adgroupstats import AdGroupStatsModel

class AdGroupModel(SQLModel, table=True):
    __tablename__ = "ad_groups"
    ad_group_id: int = Field(default=None, primary_key=True, index=True, unique=True)
    ad_group_name: str = Field(max_length=100)
    campaign_id: int = Field(foreign_key="campaigns.campaign_id")
    campaign: CampaignModel = Relationship(back_populates="ad_groups")
    ad_group_stats: List["AdGroupStatsModel"] = Relationship(back_populates="ad_group")