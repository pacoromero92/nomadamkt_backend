from datetime import datetime
from database import Base
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Column,UniqueConstraint
from sqlalchemy.orm import relationship
class Adaccount(Base):
    __tablename__ = "ad_accounts"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    name = Column(String)
    platform = Column(String, nullable=False)
    account_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    client = relationship("Clients", back_populates="ad_accounts")
    campaigns = relationship("AdCampaingns", back_populates="ad_account")
    __table_args__ = (
        UniqueConstraint('account_id'),
    )
