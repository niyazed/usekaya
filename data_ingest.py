import pandas as pd
from fastapi import Depends
from sqlmodel import Session


from src.db.database import get_session
from src.db.models import AdGroupStatsModel, CampaignModel, AdGroupModel


campaign_file  = pd.read_excel("data.xlsx", sheet_name="campaign")
ad_group_file = pd.read_excel("data.xlsx", sheet_name="ad_group")
ad_group_stats_file = pd.read_excel("data.xlsx", sheet_name="ad_group_stats")

def insert_campaign_data(session: Session = next(get_session())):
    for _, row in campaign_file.iterrows():
        campaign = CampaignModel(
            campaign_id=row['campaign_id'],
            campaign_name=row['campaign_name'], 
            campaign_type=row['campaign_type']
        )
        session.add(campaign)
    session.commit()

def insert_ad_group_data(session: Session = next(get_session())):
    for _, row in ad_group_file.iterrows():
        ad_group = AdGroupModel(
            ad_group_id=row['ad_group_id'],
            ad_group_name=row['ad_group_name'],
            campaign_id=row['campaign_id']
        )
        session.add(ad_group)
    session.commit()

def insert_ad_group_stats_data(session: Session = next(get_session())):
    for _, row in ad_group_stats_file.iterrows():
        ad_group_stats = AdGroupStatsModel(
            date=row['date'].strftime('%Y-%m-%d'),
            ad_group_id=row['ad_group_id'],
            device=row['device'],
            impressions=row['impressions'],
            clicks=row['clicks'],
            conversions=row['conversions'],
            cost=row['cost']
        )   
        session.add(ad_group_stats)
    session.commit()

if __name__ == "__main__":
    insert_campaign_data()
    insert_ad_group_data()
    insert_ad_group_stats_data()
