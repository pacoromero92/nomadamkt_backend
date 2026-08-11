from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload

from models.silver import  SilverCampaignInsights
from models.gold import GoldCampaignInsights
from database import SessionLocal
import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
def upsert_gold_insight(data: dict):
    with SessionLocal() as session:
        stmt = insert(GoldCampaignInsights).values(data)
       
        update_cols = {
            c.name: stmt.excluded[c.name] 
            for c in GoldCampaignInsights.__table__.columns
            
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=['month','year','campaign_id','adset_name'],
            set_=update_cols
        )
        session.execute(stmt)
        session.commit()

def fetch_gold():
    with SessionLocal() as session:
        silverData = session.query(SilverCampaignInsights)\
                .filter(SilverCampaignInsights.is_processed == 0)\
                .all()

    df = pd.DataFrame([
        {
            column.name: getattr(row, column.name)
            for column in SilverCampaignInsights.__table__.columns
        }
        for row in silverData
    ])
    if df.empty:
        return
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df_agg = df.groupby(['campaign_id','ad_accounts_id','adset_name','month','year'])[['impressions', 'clicks', 'spend', 'cpm', 'cpc', 'cpp', 'videos_view',
       'message_connection', 'purchase']].sum().reset_index()

    data = df_agg.to_dict(orient="records")
    upsert_gold_insight(data)