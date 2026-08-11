from models.silver import SilverCampaignInsights
from database import SessionLocal

def get_campaings(client_id,date_from,date_to,adset_name):
    with SessionLocal() as session:
        query = session.query(SilverCampaignInsights)
        
        
        if date_from:
            query = query.filter(SilverCampaignInsights.date >= date_from)
        if date_to:
            query = query.filter(SilverCampaignInsights.date <= date_to)
        if adset_name:
            query = query.filter(SilverCampaignInsights.adset_name == adset_name)
        total = query.count()
        rows = query.all()
        return {
            "data": rows,
            "total": total,
            "page": 0,
            "page_size": 0,
            "total_pages": 0  # ceil division
        }
        