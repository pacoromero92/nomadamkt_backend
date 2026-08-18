from pydantic import BaseModel
from typing import Optional
class AdAccountObject(BaseModel):
    id:int
    name:str
class ClientObject(BaseModel):
    name:str
    meta_account:str


class ClientGetObject(BaseModel):
    id:int
    name:str
    meta_account:Optional[AdAccountObject]=None

