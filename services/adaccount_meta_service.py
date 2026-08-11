from models.adaccount import Adaccount
from sqlalchemy.dialects.postgresql import insert
from database import SessionLocal  
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
FACEBOOK_URL = os.getenv('FACEBOOK_HOST_URL')
FACEBOOK_TOKEN = os.getenv('FACEBOOK_TOKEN')


def upsert_adaccounts(data):
    with SessionLocal() as session:
        stmt = insert(Adaccount).values(data)
        stmt = stmt.on_conflict_do_update(
            index_elements=['account_id'],
            set_={
                'name': stmt.excluded.name,
                'platform': stmt.excluded.platform,
            }
        )
        session.execute(stmt)
        session.commit()


def get_adaccount_facebook():
    try:
        URL = f"{FACEBOOK_URL}26199454743063577/authorized_adaccounts?fields=name,account_id"
        parametros = {
            "access_token": FACEBOOK_TOKEN,
            "fields": "id,name"  # Solicitamos solo el ID y el nombre de la cuenta
        }
        respuesta = requests.get(URL, params=parametros)
        if 'data' in respuesta.json():
            for account in respuesta.json()['data']:
                data = {
                    'name':account.get('name'),
                    'account_id':account.get('id'),
                    'platform':'META'
                }
                upsert_adaccounts(data)
    
    except Exception as error:
        raise Exception("Ocurrio un error ")