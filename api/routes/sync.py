from fastapi import APIRouter,BackgroundTasks,Depends,HTTPException
from services.adaccount_meta_service import get_adaccount_facebook
from services.adcampaings_service import fetch_campaings

router = APIRouter(prefix="/service", tags=["Services"])

@router.post("/adaccounts")
async def run_serice_facebook(background_tasks: BackgroundTasks):
    background_tasks.add_task(service_adaccounts_facebook)
    return {"message": "Proceso iniciado", "status": "running"}


def service_adaccounts_facebook():
    # tu lógica pesada aquí
    get_adaccount_facebook()
    print("Terminé")


@router.post("/campaings")
async def run_serice_facebook(background_tasks: BackgroundTasks):
    background_tasks.add_task(service_campaings_facebook)
    return {"message": "Proceso iniciado", "status": "running"}


def service_campaings_facebook():
    # tu lógica pesada aquí
    fetch_campaings()
    print("Terminé")


