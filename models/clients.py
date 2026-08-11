from database import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Column
from datetime import datetime
from sqlalchemy.orm import relationship
class Clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("UsersClients", back_populates="clients")
    ad_accounts = relationship("Adaccount", back_populates="client")    
