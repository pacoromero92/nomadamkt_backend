from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, DateTime, UniqueConstraint,ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime
from database import Base
class BronzeCampaignInsights(Base):
    __tablename__ = 'bronze_campaign_insights'

    
    id = Column(Integer, primary_key=True)
    
    date_start = Column(Date)
    adset_name = Column(String)
    ad_name = Column(String)
    raw_data = Column(JSONB)
    ingested_at = Column(DateTime, default=datetime.now)
    is_processed = Column(Integer, default=0)
    campaign_id = Column(String)
    ad_accounts_id=Column(Integer,ForeignKey("ad_accounts.id"))
    __table_args__ = (
        UniqueConstraint('campaign_id', 'date_start','adset_name','ad_name'),
    )