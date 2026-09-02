from fastapi import APIRouter,Depends,HTTPException
from auth.utils import get_current_user
from repositories.kpis_repository import get_kpis_available
from schemas.response_schema import MessageResponse,DataResponse
from schemas.auth_schema import RegisterUser
from schemas.kpi_schemas import Kpi
from repositories.users_repository import registrer_user
router = APIRouter(prefix="/settings", tags=["Settings"])
from auth.utils import has_access

@router.get("/kpis",response_model=DataResponse[Kpi])
def get_kpis(current_user=Depends(get_current_user)):
    return get_kpis_available()

@router.post("/register",response_model=MessageResponse)
async def register(data:RegisterUser,current_user=Depends(get_current_user)):
    try:
        (_,_,rol)=current_user
        if has_access(['Admin'],rol):
            return registrer_user(data.email,data.password,data.name,data.role)
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        return {
            "message":str(e),
            "status_code":500
        }