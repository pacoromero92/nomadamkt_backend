from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload
from models.adaccount import Adaccount
from models.adcampaigns import AdCampaingns
from database import SessionLocal
import os
import requests
import json
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
FACEBOOK_URL = os.getenv('FACEBOOK_HOST_URL')
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN')


def upsert_campaings(data):
    with SessionLocal() as session:
           stmt = insert(AdCampaingns).values(data)
           stmt = stmt.on_conflict_do_update(
               index_elements=['campaign_id','ad_accounts_id'],
               set_={
                   'campaign_name': stmt.excluded.campaign_name,
                   'objective': stmt.excluded.objective,
                   'start_time': stmt.excluded.start_time,
                   'end_time': stmt.excluded.end_time,
                   'status':stmt.excluded.status
               }
           )
           session.execute(stmt)
           session.commit()
          

def get_accounts():
    with SessionLocal() as session:
        rows = session.query(Adaccount)\
                    .options(joinedload(Adaccount.client))\
                    .filter(Adaccount.client_id != None)\
                    .filter(Adaccount.platform == 'META')\
                    .all()
        return rows
                    

def fetch_campaings():
    filtro_activos = [
        {
            "field": "effective_status",
            "operator": "IN",
            "value": ["ACTIVE"]  # Solo traerá las campañas activas
        }
    ]

    params = {
        "access_token": FACEBOOK_TOKEN,
        "fields": "name,id,effective_status,objective,start_time,stop_time", # Campos útiles de configuración
        "filtering": json.dumps(filtro_activos),  # Convertimos el filtro a texto JSON para la URL
        "limit": 100
    }
    accounts = get_accounts()
    record = 0
    for account in accounts:
        print(account.account_id , account.name)
        print(account.client.name)
        url_campaings = f"{FACEBOOK_URL}{account.account_id}/campaigns"


        response = requests.get(url_campaings, params=params)
        data = response.json()
        
        if data['data']:
        
            df = pd.json_normalize(data['data'])
           
            df['ad_accounts_id'] = account.id
            df['campaign_name']=df['name']
            df['objective'] = df['objective'].replace({'OUTCOME_ENGAGEMENT': 'ENGAGEMENT', 'OUTCOME_SALES': 'SALES'}).fillna(df['objective'])
            df['status']=df['effective_status']
            df['campaign_id']=df['id']
            df['end_time']=df['stop_time']
            df.drop(
                columns=["name", "effective_status", "stop_time","id"],
                inplace=True
            )
            df = df.reset_index(drop=True)
            lenght = len(df)
            record=record+lenght
            df = df.where(pd.notnull(df), None)
            data = df.to_dict(orient="records")
            upsert_campaings(data)
    return record 