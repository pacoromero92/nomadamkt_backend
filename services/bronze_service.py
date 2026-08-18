from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload
from models.adaccount import Adaccount
from models.adcampaigns import AdCampaingns
from models.bronze import BronzeCampaignInsights
from database import SessionLocal
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
FACEBOOK_URL = os.getenv('FACEBOOK_HOST_URL')
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN')

def upsert_insight(data: dict):
    with SessionLocal() as session:
        stmt = insert(BronzeCampaignInsights).values(data)
        stmt = stmt.on_conflict_do_update(
            index_elements=['campaign_id', 'date_start',"adset_name","ad_name"],
            set_={
                'raw_data': stmt.excluded.raw_data,
                'ingested_at': stmt.excluded.ingested_at,
                'is_processed': stmt.excluded.is_processed,
                'ad_accounts_id':stmt.excluded.ad_accounts_id,
            }
        )
        session.execute(stmt)
        session.commit()

def get_accounts():
    with SessionLocal() as session:
         accounts = session.query(Adaccount)\
                    .options(joinedload(Adaccount.client))\
                    .options(joinedload(Adaccount.campaigns))\
                    .filter(Adaccount.client_id != None)\
                    .filter(Adaccount.platform == 'META')\
                    .all()
         return accounts

def fetch_to_bronze():
    accounts =  get_accounts()
    read_records  = 0
    for account in accounts:
        campaigns_id = []
        for campaing in account.campaigns:
            campaigns_id.append(campaing.campaign_id)
        
       
        url_ads = f'{FACEBOOK_URL}{account.account_id}/insights'
       
        filter =[
                {
                    "field": "campaign.id",
                    "operator": "IN",
                    "value": campaigns_id  # Solo traerá las campañas activas
                }
            ]
        parametos = {
            "access_token": FACEBOOK_TOKEN,
            "fields": "campaign_name,impressions,clicks,spend,campaign_id,adset_name,cpm,cpp,cpc,actions,cost_per_action_type,ad_name",   
            "level": "ad"  ,
            #"date_preset":"yesterday",
            "filtering":json.dumps(filter)   ,
            'time_increment': 1,
            "limit": 100   ,
            "time_range": json.dumps({
                "since": "2026-08-01",
                "until": "2026-08-31"
            })
            }
        i=0
        while url_ads:
        
            response = requests.get(url=url_ads,params=parametos)
            resp = response.json()
           
            if 'data' in resp:
                    
                    for row in resp['data'] :
                        read_records=read_records+1
                        data = {
                            'campaign_id': row['campaign_id'],
                            'date_start': row['date_start'],
                            'raw_data': row,  # todo el dict va aquí
                            'is_processed': 0,
                            'adset_name':row['adset_name'],
                            'ad_name':row['ad_name'],
                            'ad_accounts_id':account.id
                           
                        }
                        upsert_insight(data)
            url_ads = resp.get("paging", {}).get("next") 
            parametos = None
    print(read_records)
    return read_records



