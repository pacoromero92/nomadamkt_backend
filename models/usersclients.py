from database import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Column
from datetime import datetime
from sqlalchemy.orm import relationship
class UsersClients(Base):
    __tablename__ = "users_clients"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    users = relationship("Users", back_populates="clients")
    clients = relationship("Clients", back_populates="users")