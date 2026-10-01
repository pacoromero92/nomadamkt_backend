from fastapi import APIRouter,Depends,HTTPException
from repositories.clients_repository import get_client
from repositories.dashboard_repository import get_kpis_values,get_gold_table
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/{id}")
def get_client_info(id,month,year):
    client = get_client(id)['data']
    kpis = get_kpis_values(id,month,year,client.show_kpis)
    return {'kpis':kpis}


@router.get("/{id}/campaings")
def get_general_campaings(id,month,year):
    client = get_client(id)['data']
    gold = get_gold_table(client.meta_account.id,month,year)
    return {'data':gold}