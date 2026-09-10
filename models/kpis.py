from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.orm import relationship
from database import Base
class Kpis(Base):
    __tablename__ = 'kpis'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    visible = Column(Boolean, default=True)
    code = Column(String)
    clients = relationship(
        "Clients",
        secondary="kpis_clients",
        back_populates="kpis"
    )
