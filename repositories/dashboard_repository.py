from database import SessionLocal
from fastapi.exceptions import HTTPException
from models.gold_kpis import GoldKpis
from models.gold_campaings import GoldCampaingsinsights
from models.kpis import Kpis
def get_kpis_values(id_client,month,year,id_kpis):
    previous_month = int(month)-1
    previous_year = int(year)
    array = []
    if previous_month<=0:
        previous_month=12
        previous_year=previous_year-1
    with SessionLocal() as  session:
       
        
        kpis = session.query(Kpis.id,Kpis.name,GoldKpis.value
                             ).join(
                                 Kpis,GoldKpis.id_kpi==Kpis.id
                            ).where(
                                    GoldKpis.id_client==id_client,
                                    GoldKpis.month==month,
                                    GoldKpis.year==year,
                                    GoldKpis.id_kpi.in_(id_kpis)
                            ).all()
    print(previous_month,previous_year)
    for kpi in kpis:
        prev_value = get_value_prev(id_client,previous_month,previous_year,kpi.id)
        if prev_value:
           
            porcentage = ((kpi.value - prev_value)/prev_value)*100
        else :
           
            porcentage = 'N/A'
        array.append({
               'name': kpi.name,
               'value':kpi.value,
               'previous_value':prev_value,
               'porcentage':porcentage
        }) 
    return array

def get_value_prev(id_client,month,year,id_kpi):
    with SessionLocal() as session:
        prev_value =session.query(GoldKpis.value).where(
                GoldKpis.id_client==id_client,
                GoldKpis.month==month,
                GoldKpis.year==year,
                GoldKpis.id_kpi==id_kpi).first()
        if prev_value:
            return prev_value.value
        return None

def get_gold_table(id_client,month,year):
    with SessionLocal() as session:
        gold = session.query(GoldCampaingsinsights).where(
            GoldCampaingsinsights.month==month,
            GoldCampaingsinsights.year==year,
            GoldCampaingsinsights.ad_accounts_id==id_client
        ).all()
       
        return gold