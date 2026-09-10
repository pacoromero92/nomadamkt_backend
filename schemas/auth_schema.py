from pydantic import BaseModel

class RegisterUser(BaseModel):
    email:str
    password:str
    name:str
    rol:str

class LoginSchema(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id:int 
    name:str
    email:str
    rol:str