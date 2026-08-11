from pydantic import BaseModel

class RegisterUser(BaseModel):
    email:str
    password:str
    name:str

class LoginSchema(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    name:str
    email:str
    rol:str