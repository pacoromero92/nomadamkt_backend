from fastapi import APIRouter,HTTPException,Depends
from datetime import date
from typing import Optional
from repositories.users_repository import registrer_user,login
from auth.utils import get_refresh_token
from schemas.response_schema import PaginatedResponse,MessageResponse,LoginSchemaResponse
from schemas.auth_schema import RegisterUser,LoginSchema
from typing import Union
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register",response_model=MessageResponse)
async def register(data:RegisterUser):
    try:
        return registrer_user(data.email,data.password,data.name)
    except Exception as e:
        return {
            "message":str(e),
            "status_code":500
        }
    
@router.post("/login",response_model=Union[LoginSchemaResponse,MessageResponse])
async def login_api(data:LoginSchema):
    try:
        return login(data.email,data.password)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
    
@router.post("/refresh")
async def refresh_api(
    current_user=Depends(get_refresh_token)
):
    return current_user