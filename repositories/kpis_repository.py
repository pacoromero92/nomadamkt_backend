from models.kpis import Kpis
from database import SessionLocal
from fastapi import HTTPException
def get_kpis_available():
    with SessionLocal() as session:
        query = session.query(Kpis)
        return {
            "data":query.all()
        }

def create_kpi(name:str,visible:bool,code:str):
    with SessionLocal() as session:
        kpi = Kpis(
            name =  name,
            visible = visible,
            code = code
        )
        session.add(kpi)
        session.commit()
        return {"message": "Kpi creada","status_code":202}

def edit_kpi(id:str,name:str,visible:bool,code:str):
    with SessionLocal() as session:
        kpi =   session.query(Kpis).filter(Kpis.id==id).first()
        if not kpi:
            raise HTTPException(status_code=500,detail="No Client Found")
        kpi.name=name
        kpi.visible = visible
        kpi.code = code
        session.commit()
        return {"message": "Kpi Editado","status_code":202}