from pydantic import BaseModel
from typing import Generic, TypeVar, List
T = TypeVar('T')
class UserResponse(BaseModel):
    name:str
    email:str
    rol:str
class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

class MessageResponse(BaseModel):
    message :str
    status_code :int

class LoginSchemaResponse(BaseModel,Generic[T]):
    access_token:str
    refresh_token:str
    status_code:int
    user:UserResponse
    
class TaskResponse(BaseModel):
    message:str
    status:str
    task_id:str



class ObjectRespose(BaseModel,Generic[T]):
        data: T


