from sqlmodel import SQLModel, Field, Relationship
from typing import List
from sqlalchemy import BigInteger, Numeric
from decimal import Decimal


class CampaignModel(SQLModel, table=True):
    __tablename__ = "campaigns"
    campaign_id: int = Field(sa_type=BigInteger(), primary_key=True, index=True, unique=True)
    campaign_name: str = Field(max_length=100)
    campaign_type: str = Field(max_length=50)
    ad_groups: List["AdGroupModel"] = Relationship(back_populates="campaign")


class AdGroupModel(SQLModel, table=True):
    __tablename__ = "ad_groups"
    ad_group_id: int = Field(sa_type=BigInteger(), primary_key=True, index=True, unique=True)
    ad_group_name: str = Field(max_length=100)
    campaign_id: int = Field(sa_type=BigInteger(), foreign_key="campaigns.campaign_id")
    campaign: CampaignModel = Relationship(back_populates="ad_groups")
    ad_group_stats: List["AdGroupStatsModel"] = Relationship(back_populates="ad_group")


class AdGroupStatsModel(SQLModel, table=True):
    __tablename__ = "ad_group_stats"
    ad_group_stats_id: int = Field(default=None, primary_key=True, index=True, unique=True)
    date: str = Field(max_length=10)
    ad_group_id: int = Field(sa_type=BigInteger(), foreign_key="ad_groups.ad_group_id")
    device: str = Field(max_length=50)
    impressions: int
    clicks: int
    conversions: int
    cost: Decimal = Field(sa_type=Numeric(10, 2))
    ad_group: AdGroupModel = Relationship(back_populates="ad_group_stats")

