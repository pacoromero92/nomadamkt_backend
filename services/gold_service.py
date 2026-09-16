from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload
from models.gold_campaings import GoldCampaingsinsights
from models.silver import  SilverCampaignInsights
from models.kpis import Kpis
from models.gold_kpis import GoldKpis
from models.adaccount import Adaccount
from database import SessionLocal
from dotenv import load_dotenv
import pandas as pd
import numpy as np

def run_gold_process():
    df = get_silver_records()
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['lead']=df['leads']
    df_agg = df.groupby(['campaign_id','ad_name','adset_name','month','year','ad_accounts_id'])[['impressions', 'clicks', 'spend', 'cpm', 'cpc', 'cpp', 'videos_view',
       'message_connection', 'purchase','lead']].sum().reset_index()

    if df_agg.empty:
        raise Exception("Silver doesn't have records")

    data = df_agg.to_dict(orient="records")
    upsert_gold_insight(data)
    df_kpi = df.groupby(['month','year','ad_accounts_id'])[['impressions', 'clicks', 'spend', 'cpm', 'cpc', 'cpp', 'videos_view',
       'message_connection', 'purchase','leads']].sum().reset_index()
    kpis = get_kpis()
    if not kpis:
        raise Exception("There are no kpis configured")

    data=[]
    for index, row in df_kpi.iterrows():
        for kpi in kpis:
            kpi_id = kpi['id']
            column = kpi['code']
            value = getattr(row, column, 0) if column else 0
            data.append ({
                'month':row['month'],
                'year':row['year'],
                'id_kpi':kpi_id,
                'value':value,
                'id_client':get_client_id(row['ad_accounts_id'])
        })
    upsert_kpi_values(data)
    with SessionLocal() as session:
        ids = df["id"].tolist()

        session.query(SilverCampaignInsights).filter(
            SilverCampaignInsights.id.in_(ids)
        ).update(
            {SilverCampaignInsights.is_processed: 1},
            synchronize_session=False
        )

        session.commit()


def get_kpis():
    with SessionLocal() as session:
        rows = session.query(Kpis).all()
        kpis = [
            {
                'id':row.id,
                'name':row.name,
                'code':row.code
            }
            for row in rows
        ]
    return kpis

def upsert_gold_insight(data: dict):
    with SessionLocal() as session:
        stmt = insert(GoldCampaingsinsights).values(data)
       
        update_cols = {
            c.name: stmt.excluded[c.name] 
            for c in GoldCampaingsinsights.__table__.columns
            
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=['month','year','campaign_id','adset_name','ad_name'],
            set_=update_cols
        )
        session.execute(stmt)
        session.commit()
def upsert_kpi_values(data: dict):
    with SessionLocal() as session:
        stmt = insert(GoldKpis).values(data)
       
        update_cols = {
            c.name: stmt.excluded[c.name] 
            for c in GoldKpis.__table__.columns
            
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=['month','year','id_kpi','id_client'],
            set_=update_cols
        )
        session.execute(stmt)
        session.commit()

def get_client_id(id_account):
    with SessionLocal() as session:
        account = session.query(Adaccount).filter(Adaccount.id==id_account).first()

    return account.client_id


def get_silver_records():
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
    return df

if __name__ == "__main__":
   
    
    run_gold_process()