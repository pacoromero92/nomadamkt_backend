from sqlalchemy import create_engine, Column, Integer, String,  DateTime, UniqueConstraint,ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base,relationship

from datetime import datetime
from database import Base
class AdCampaingns(Base):
    __tablename__ = 'ad_campaings'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(String)
    campaign_name= Column(String)
    objective = Column(String)
    start_time=Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String)
    ad_accounts_id=Column(Integer,ForeignKey("ad_accounts.id"))
    ad_account = relationship("Adaccount", back_populates="campaigns")
    last_update=Column(DateTime, default=datetime.now)
    __table_args__ = (
        UniqueConstraint('campaign_id','ad_accounts_id'),
    )