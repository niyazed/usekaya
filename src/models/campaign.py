from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from adgroup import AdGroupModel

class CampaignModel(SQLModel, table=True):
    __tablename__ = "campaigns"
    campaign_id: int = Field(default=None, primary_key=True, index=True, unique=True)
    campaign_name: str = Field(max_length=100)
    campaign_type: str = Field(max_length=50)
    ad_groups: List["AdGroupModel"] = Relationship(back_populates="campaign")






