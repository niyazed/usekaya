from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from adgroup import AdGroupModel

class AdGroupStatsModel(SQLModel, table=True):
    __tablename__ = "ad_group_stats"
    ad_group_stats_id: int = Field(default=None, primary_key=True, index=True, unique=True)
    date: str = Field(max_length=10)
    ad_group_id: int = Field(foreign_key="ad_groups.ad_group_id")
    device: str = Field(max_length=50)
    impressions: int
    clicks: int
    conversions: int
    cost: float
    ad_group: AdGroupModel = Relationship(back_populates="ad_group_stats")