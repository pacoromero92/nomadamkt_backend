from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from models.usersclients import UsersClients
from sqlalchemy import Enum as SQLEnum
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    name = Column(String)
    role = Column(String,nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_verified = Column(Boolean, default=False)
    clients = relationship("UsersClients", back_populates="users")