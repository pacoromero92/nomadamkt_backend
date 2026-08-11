from fastapi import APIRouter
from datetime import date
from typing import Optional
from repositories.insights_repository import get_campaings
from schemas.response_schema import PaginatedResponse
from schemas.insights_schema import CampaignDailyResponse
router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("/campaigns",response_model=PaginatedResponse[CampaignDailyResponse])
async def get_campaign( 
    client_id:int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    adset_name: Optional[str] = None):
    return get_campaings(date_from=date_from,date_to=date_to,adset_name=adset_name)
@router.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: str):
    pass

@router.get("/campaigns/{campaign_id}/daily")
async def get_campaign_daily(campaign_id: str):
    pass

@router.get("/campaigns/{campaign_id}/summary")
async def get_campaign_summary(campaign_id: str):
    pass