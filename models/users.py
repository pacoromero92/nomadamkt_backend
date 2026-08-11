from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from models.usersclients import UsersClients
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    rol = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    clients = relationship("UsersClients", back_populates="users")