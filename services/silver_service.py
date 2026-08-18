
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.dialects.postgresql import insert
from models.bronze import BronzeCampaignInsights
from models.silver  import SilverCampaignInsights
from database import SessionLocal


def upsert_silver_insight(data: dict):
    with SessionLocal() as session:
        stmt = insert(SilverCampaignInsights).values(data)
       
        update_cols = {
            c.name: stmt.excluded[c.name] 
            for c in SilverCampaignInsights.__table__.columns
            
        }
        stmt = stmt.on_conflict_do_update(
            index_elements=['campaign_id', 'date',"adset_name","ad_name"],
            set_=update_cols
        )
        session.execute(stmt)
        session.commit()



def process_to_silver():
    with SessionLocal() as session:
        rows = session.query(BronzeCampaignInsights)\
            .filter(BronzeCampaignInsights.is_processed == 0)\
            .all()
        read_records  = 0
        for row in rows:
            # extraes los datos del raw_data
            read_records = read_records+1
            row_json = row.raw_data
            message_connection = 0
            cost_per_message =0.0
            views_view =0
            purchase = 0
            cost_per_sale =0.0
            actions = row_json.get('actions',[])
            cost_actions = row_json.get('cost_per_action_type',[])
            for action in actions:
                if action['action_type']=='video_view':
                   
                    views_view = action['value']
                if action['action_type']=='onsite_conversion.total_messaging_connection':
                  
                    message_connection = action['value']
                if action['action_type']=='purchase':
                                  
                    purchase = action['value']
            for action in cost_actions:
                
                if action['action_type']=='onsite_conversion.total_messaging_connection':
                    
                    cost_per_message = action['value']
                if action['action_type']=='purchase':
                                    
                    cost_per_sale = action['value']
                        
            data = {
                "campaign_id":row_json.get("campaign_id"),
                "campaign_name":row_json.get("campaign_name"),
                "date":row_json.get("date_start"),
                "adset_name":row_json.get("adset_name"),
                "ad_name":row_json.get("ad_name"),
                "impressions":row_json.get("impressions",0),
                "clicks":row_json.get("clicks",0),
                "cpm":row_json.get("cpm",0),
                "cpp":row_json.get("cpp",0),
                "cpc":row_json.get('cpc',0),
                "spend":row_json.get("spend",0),
                "videos_view" : views_view,
                "message_connection":message_connection,
                "purchase":purchase,
                "cost_per_message":cost_per_message,
                "cost_per_sale":cost_per_sale,
                'ad_accounts_id':row.ad_accounts_id
            }
            upsert_silver_insight(data)
        
            
            # marcas como procesado
            row.is_processed = 1
        
        session.commit()  # un solo commit al final
        return read_records
    

if __name__ == "__main__":
   
    
    process_to_silver()