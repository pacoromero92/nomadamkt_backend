from fastapi import APIRouter,Depends,HTTPException
import time
from datetime import datetime
from typing import Optional
from repositories.clients_repository import create_clients,get_clients,get_adaccounts,edit_client,get_client

from schemas.response_schema import PaginatedResponse,MessageResponse,ObjectRespose
from schemas.client_schema import ClientObject,ClientGetObject,AdAccountObject
from auth.utils import has_access
from typing import Union
from auth.utils import get_current_user,has_access
from models.Role import Role
router = APIRouter(prefix="/client", tags=["Clients"])

@router.get("/",response_model=PaginatedResponse[ClientGetObject])
def get_clients_api(
    current_user=Depends(get_current_user)
):
    try:
        id_user=current_user        
        if has_access(id_user=id_user,roles=[Role.ADMIN]):
            return get_clients()
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        raise HTTPException(500,"Error")

@router.post("/")
def post_client(data:ClientObject, current_user=Depends(get_current_user)):
    try:
        id_user=current_user        
        if has_access(id_user=id_user,roles=[Role.ADMIN]):
            return create_clients(name=data.name,meta_addacount=data.meta_account,kpis=data.show_kpis)
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        raise HTTPException(500,"Error")
       
    

@router.get("/adaccounts",response_model=PaginatedResponse[AdAccountObject])
async def get_unassign_adaccounts(
     current_user=Depends(get_current_user)
):
    try:
        id_user=current_user        
        if has_access(id_user=id_user,roles=[Role.ADMIN]):
            return get_adaccounts()
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        raise HTTPException(500,"Error")



@router.put("/{id}")
def put_client(id:str,
               data:ClientObject, 
               current_user=Depends(get_current_user)):
    
    try:
        id_user=current_user        
        if has_access(id_user=id_user,roles=[Role.ADMIN]):
            return edit_client(id,data.name,data.meta_account,data.show_kpis)
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        raise HTTPException(500,"Error")



@router.get("/{id}",response_model=ObjectRespose[ClientGetObject])
def get_client_api(id:str,
                    current_user=Depends(get_current_user)
                    ):
    try:
        id_user=current_user        
        if has_access(id_user=id_user,roles=[Role.ADMIN]):
           return get_client(id)
    except HTTPException as e:
        raise HTTPException(e.status_code,e.detail)
    except Exception as e:
        raise HTTPException(500,"Error")
   
        
    



