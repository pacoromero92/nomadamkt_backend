from models.clients import Clients
from models.adaccount import Adaccount
from models.silver import SilverCampaignInsights
from database import SessionLocal
from fastapi.exceptions import HTTPException
def create_clients(name:str,meta_addacount:int):
   with SessionLocal() as session:
        try:
            client = Clients(
                name=name
            )
            session.add(client)
            session.commit()
            session.refresh(client)
            assign_ad(meta_addacount,client.id)
            return {"message": "Ciente Creado","status_code":202}
        except Exception:
                raise Exception()
   

def edit_client(id:int,name:str,meta_addacount:int):
    try:
        with SessionLocal() as session:
            client = session.query(Clients).filter(Clients.id==id).first()
            client.name=name
            session.commit()
            assign_ad(meta_addacount,id)
    
    except Exception:
        raise Exception()
def assign_ad(adaccount_id:int,client_id):
    print(adaccount_id,client_id)
    with SessionLocal() as session:
        addaccount = session.query(Adaccount).filter(Adaccount.id==adaccount_id).first()
        print(addaccount)
        addaccount.client_id = client_id
        session.commit()

def get_client(id:int):
    try :
        with SessionLocal() as session:
            client = session.query(Clients).filter(Clients.id==id).first()
            if client == None:
                raise HTTPException(status_code=404,detail="Client not found")
            for ad in client.ad_accounts:
                if ad.platform=='Facebook':
                    client.meta_account=ad
            return {"data":client}
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as error:
        print(error)
        raise Exception("Error getting client")

def get_clients(id_user = None):
    with SessionLocal() as session:
        query = session.query(Clients)
    
            
        total = query.count()
        rows = query.all()
        for row in rows:
            row.meta_account=None
            for ad in row.ad_accounts:
                if ad.platform=='META':
                    row.meta_account=ad

        return {
            "data": rows,
            "total": total,
            "page": 0,
            "page_size": 0,
            "total_pages": 0  # ceil division
        }
    
def get_adaccounts():
    with SessionLocal() as session:
        query = session.query(Adaccount).filter(Adaccount.client_id == None )
        total = query.count()
        rows = query.all()
        return {
            "data": rows,
            "total": total,
            "page": 0,
            "page_size": 0,
            "total_pages": 0  # ceil division
        }




