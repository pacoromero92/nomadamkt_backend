from fastapi import APIRouter,Depends,HTTPException
from auth.utils import get_current_user
from repositories.kpis_repository import get_kpis_available,create_kpi,edit_kpi
from schemas.response_schema import MessageResponse,DataResponse
from schemas.auth_schema import RegisterUser,UserResponse,TokenSchema
from schemas.kpi_schemas import Kpi
from repositories.users_repository import registrer_user,list_users,activate_user,reset_password
from models.Role import Role
router = APIRouter(prefix="/settings", tags=["Settings"])
from auth.utils import has_access

@router.get("/kpis",response_model=DataResponse[Kpi])
def get_kpis(current_user=Depends(get_current_user)):
    return get_kpis_available()

@router.get("/users",response_model=DataResponse[UserResponse])
def get_users(current_user=Depends(get_current_user)):
    return list_users()

@router.post("/user",response_model=MessageResponse)
async def register(data:RegisterUser,current_user=Depends(get_current_user)):
    try:
        id_user=current_user
        
        if has_access(roles=[Role.ADMIN],id_user=id_user):
            return registrer_user(data.email,data.name,data.role)
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        return {
            "message":str(e),
            "status_code":500
        }

@router.post("/user/activate")
async def user_activate(data:TokenSchema):
    return activate_user(token=data.token,password=data.password)

@router.get("/user/forgot/{id}")
async def user_forgot(id,current_user=Depends(get_current_user)):
    if has_access(current_user,[Role.ADMIN]):
        return reset_password(id)
    

@router.post("/kpis",response_model=MessageResponse)
def addkpi(data:Kpi,current_user=Depends(get_current_user)):
    try:
        id_user=current_user   
        if has_access(id_user=id_user,roles=[Role.ADMIN]):
            return create_kpi(data.name,True,data.code)
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        print(e)
        raise HTTPException(500,"Error")

@router.put("/kpis/{id}",response_model=MessageResponse)
def editkpi(id:int,data:Kpi,current_user=Depends(get_current_user)):
    try:
        id_user=current_user
        if has_access(id_user=id_user,roles=[Role.ADMIN]):
            return edit_kpi(id,data.name,True,data.code)
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        print(e)
        raise HTTPException(500,"Error")

