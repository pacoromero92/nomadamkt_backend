from models.clients import Clients
from models.adaccount import Adaccount
from models.silver import SilverCampaignInsights
from models.kpis_clients import Kpis_Clients
from database import SessionLocal
from fastapi.exceptions import HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete
def create_clients(name:str,meta_addacount:int,kpis:list=None):
   with SessionLocal() as session:
        try:
            client = Clients(
                name=name
            )
            session.add(client)
            
            
            session.flush()
            if meta_addacount:
                assign_ad(meta_addacount,client.id,session)
            
            if kpis:
                assign_kpis(client.id,kpis)
            session.commit()
            return {"message": "Ciente Creado","status_code":202}
        except Exception as e:
            print(e)
            session.rollback()
            raise HTTPException(500,"Error creating Client ")
   

def edit_client(id:int,name:str,meta_addacount:int,kpis:list=None):
    try:
        with SessionLocal() as session:
            client = session.query(Clients).filter(Clients.id==id).first()
            client.name=name
           
            if meta_addacount:
                assign_ad(meta_addacount,id,session)
           
            if kpis:
                assign_kpis(id,kpis)
            session.commit()
            return {"message": "Ciente Editado","status_code":202}
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(500,"Error creating Client ")

def assign_ad(adaccount_id:int,client_id,session):
    print(adaccount_id,client_id)
    
    addaccount = session.query(Adaccount).filter(Adaccount.id==adaccount_id).first()
    
    addaccount.client_id = client_id
       

def assign_kpis(client_id,id_kpis=[]):
    try:
        data=[]
        for kpi in id_kpis:
            data.append({"id_client":client_id,"id_kpi":kpi})
        with SessionLocal() as session:
            session.execute(
                delete(Kpis_Clients)
                .where(
                    Kpis_Clients.id_client == client_id,
                   
                )
            )

            smt = insert(Kpis_Clients).values(data)
            smt = smt.on_conflict_do_nothing()
            result = session.execute(smt)
            session.commit()
    except Exception as e:
      
        print(e)
        
        

def get_client(id:int):
    try :
        with SessionLocal() as session:
            client = session.query(Clients).filter(Clients.id==id).first()
            if client == None:
                raise HTTPException(status_code=404,detail="Client not found")
            for ad in client.ad_accounts:
                if ad.platform=='META':
                    client.meta_account=ad
            print(client.kpis)
            client.show_kpis =[]
            for kpi in client.kpis:
                client.show_kpis.append(kpi.id)
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




