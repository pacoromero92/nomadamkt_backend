from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWEInvalidAuth,ExpiredSignatureError
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status,Depends
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY_REFRESH_TOKEN = os.getenv("SECRET_KEY_REFRESH_TOKEN")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
REFRESH_TOKEN_EXPIRE_DAYS = 1 
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)
pwd_context = CryptContext(    schemes=["argon2"],
    deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_refresh_token(token:str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    access_token = create_access_token(payload)
    return {"access_token":access_token}
async def get_current_user( token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Expiration time",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        rol = payload.get("rol",'user')
        email = payload.get("email")
        if id is None or email is None:
            raise credentials_exception
        
    except JWEInvalidAuth:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ExpiredSignatureError :
        raise credentials_exception
    except Exception as e:
        print(e)
        raise Exception
    
    return id,rol,email 


def has_access(rols=[],actual_rol=""):
    if actual_rol in rols:
        return True
    else :
        raise HTTPException(status_code=403,detail="You don't hace permission to access!")