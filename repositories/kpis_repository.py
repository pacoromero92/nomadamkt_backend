from models.kpis import Kpis
from database import SessionLocal

def get_kpis_available():
    with SessionLocal() as session:
        query = session.query(Kpis)
        return {
            "data":query.all()
        }