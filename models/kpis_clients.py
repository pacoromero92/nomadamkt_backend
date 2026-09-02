from sqlalchemy import Column,Integer,ForeignKey,UniqueConstraint
from database import Base
class Kpis_Clients(Base):
    __tablename__ = 'kpis_clients'
   
    id_client = Column(Integer,ForeignKey("clients.id"),primary_key=True)
    id_kpi = Column(Integer,ForeignKey("kpis.id"),primary_key=True)
    