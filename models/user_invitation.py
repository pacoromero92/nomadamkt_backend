from database import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Column
from datetime import datetime

class UserInvitations(Base):
    __tablename__ = "user_invitations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token_hash = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)