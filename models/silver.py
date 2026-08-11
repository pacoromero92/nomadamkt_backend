from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, DateTime, UniqueConstraint,Float,ForeignKey,BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime
from database import Base
class SilverCampaignInsights(Base):
    __tablename__ = 'silver_campaign_insights'
    id = Column(BigInteger, primary_key=True)
    
    campaign_name = Column(String)
    adset_name = Column(String)
    ad_name = Column(String)
    date = Column(Date)
    impressions = Column(Numeric,default=0)
    clicks = Column(Numeric,default=0)
    spend = Column(Float,default=0)
    cpm =Column(Float,default=0.0)
    cpc =Column(Float,default=0.0)
    cpp = Column(Float,default=0.0)
    videos_view = Column(Numeric)
    message_connection =  Column(Numeric)
    purchase = Column(Numeric)
    cost_per_message = Column(Float,default=0.0)
    cost_per_sale = Column(Float,default=0.0)
    ingested_at = Column(DateTime, default=datetime.now)
    is_processed = Column(Integer, default=0)
    campaign_id = Column(String)
    ad_accounts_id=Column(Integer,ForeignKey("ad_accounts.id"))

    __table_args__ = (
        UniqueConstraint('campaign_id', 'date','adset_name','ad_name'),
    )
