from pydantic import BaseModel
from datetime import date
class CampaignDailyResponse(BaseModel):
    campaign_id: str
    campaign_name: str
    date: date
    impressions: int
    clicks: int
    spend: float
    adset_name :str
    cpm : float
    cpp :float
    videos_view:int
    message_connection:int
    class Config:
        from_attributes = True