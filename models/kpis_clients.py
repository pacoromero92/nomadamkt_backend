from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from database import Base
class Kpis_Clients(Base):
    __tablename__ = 'kpis_clients'
    id = Column(Integer,primary_key=True)
    id_client = Column(Integer,ForeignKey("clients.id"))
    id_kpi = Column(Integer,ForeignKey("kpis.id"))