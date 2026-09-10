from pydantic import BaseModel

class Kpi(BaseModel):
    id:int= None
    name:str
    code:str


