from pydantic import BaseModel
from models.Role import Role
class RegisterUser(BaseModel):
    email:str
    name:str
    role:str

class LoginSchema(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id:int 
    name:str
    email:str
    role:Role

class TokenSchema(BaseModel):
    token:str
    password:str