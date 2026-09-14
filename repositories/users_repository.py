from models.users import Users
from models.user_invitation import UserInvitations
from database import SessionLocal
from auth.utils import hash_password, verify_password, create_access_token,create_refresh_token
from fastapi import HTTPException
import hashlib
import secrets
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
def login(email:str,password:str):
    with SessionLocal() as session:
        user = session.query(Users).filter(
             Users.email==email,
             Users.is_active==True).first()
        if not user or not verify_password(password, user.hashed_password):
                raise Exception("Usuario o Credenciales incorrectas")
        token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        return {"access_token": token, "refresh_token": refresh_token,"status_code":200,"user":user}

    return {"access_token": token, "token_type": "bearer"}

def registrer_user(email:str,name:str,role:str):
    with SessionLocal() as session:
        if session.query(Users).filter(Users.email==email).first():
            raise Exception("Usuario ya registrado")
        user = Users(
            email = email,
            name = name,
            role=role,
            is_active = 0,
            is_verified = 0
        )
        session.add(user)
       
        session.flush()
       
        (token,tokenhash) = generate_url_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)
        user_invitation = UserInvitations(
            user_id=user.id,
            token_hash=tokenhash,
            expires_at=expires_at
        )
        session.add(user_invitation)
        session.commit()
        print(f"http://localhost:8000/activate-account?token={token}")
        return {"message": "Usuario creado","status_code":202}

def list_users():
     print("here")
     with SessionLocal() as session:
          users = session.query(Users).all()
          
          return {
               "data":users
          }

def activate_user(token,password):
    with SessionLocal() as session:
        activation  = session.query(UserInvitations).filter(
             UserInvitations.expires_at>datetime.utcnow(),
             UserInvitations.used_at.is_(None)).first()
        print(hash_password(token))
        if not activation :
            raise HTTPException(status_code=400,detail="Token Expirado o Invalido")
        if not verify_password(token,activation.token_hash):
             raise HTTPException(status_code=400,detail="Token Expirado o Invalido")
        activation.used_at  = datetime.utcnow()
        user = session.query(Users).filter(
             Users.id ==activation.user_id
        ).first()
        if not user:
             raise HTTPException(status_code=500,detail="Internal Server Error")
        print(password)
        user.hashed_password=hash_password(password=password)
        user.is_active =True
        user.is_verified=True
        session.commit()
        return {"message": "Contraseña Creada","status_code":202} 

def generate_url_token():
    token = secrets.token_urlsafe(32)
    token_hash = hash_password(token)
    return token,token_hash      

def edit_user(id,data):
    try:
        with SessionLocal() as session:
            user = session.query(Users).filter(
                Users.id==id
            ).first()
            if not user:
                raise HTTPException(status_code=404,detail="Usuario no encontrado")
            if data.email != user.email:
                user.email = data.email
                user.is_verified = False
            user.name = data.name
            user.role = data.role
            session.commit()
            return {"message": "Usuario editado con exito","status_code":202}  
    except SQLAlchemyError as e:
        print(e)
        raise HTTPException(status_code=500,detail="Internal Server Error")
         

def reset_password(id_user):
    with SessionLocal() as  session:
        user =  session.query(Users).filter(
             Users.id == id_user
        ).first()
        if not user:
             raise HTTPException(status_code=404,detail="Usuario no encontrado")
        (token,tokenhash) = generate_url_token()
        expires_at = datetime.utcnow() + timedelta(hours=1)
        user_invitation = UserInvitations(
            user_id=id_user,
            token_hash=tokenhash,
            expires_at=expires_at
        )
        session.add(user_invitation)
        print(token)
        session.commit()