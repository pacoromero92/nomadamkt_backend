from sqlalchemy import  Column, Integer, String, Date, Numeric, DateTime, UniqueConstraint,ForeignKey,BigInteger
from database import Base

class GoldCampaingsinsights(Base):
    __tablename__ = 'gold_campaign_insights'
    id = Column(BigInteger, primary_key=True)
    campaign_id = Column(BigInteger,nullable=False)
    ad_name	 =  Column(String,nullable=False)

    adset_name	 =  Column(String,nullable=False)
    month	= Column(Integer,nullable=False)
    year	 = Column(Integer,nullable=False)
    impressions	=Column(Integer)
    clicks	= Column(Integer)
    spend	= Column(Numeric)
    cpm	 = Column(Numeric)
    cpc	 = Column(Numeric)
    cpp	 = Column(Numeric)
    videos_view	= Column(Integer)
    message_connection	= Column(Integer)
    purchase = Column(Integer)
    lead = Column(Numeric)
    cost_per_message = Column(Numeric)
    cost_per_purchase = Column(Numeric)
    cost_per_lead  = Column(Numeric)
    ad_accounts_id=Column(Integer,ForeignKey("ad_accounts.id"))
    __table_args__ = (
            UniqueConstraint('campaign_id', 'year','month','ad_name','adset_name'),
        )