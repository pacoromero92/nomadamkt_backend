from models.users import Users
from database import SessionLocal
from auth.utils import hash_password, verify_password, create_access_token,create_refresh_token

def login(email:str,password:str):
    with SessionLocal() as session:
        user = session.query(Users).filter(Users.email==email).first()
        if not user or not verify_password(password, user.hashed_password):
                raise Exception("Credenciales incorrectas")
        token = create_access_token({"sub": str(user.id), "email": user.email,'rol':user.rol})
        refresh_token = create_refresh_token({"sub": str(user.id), "email": user.email,'rol':user.rol})
        return {"access_token": token, "refresh_token": refresh_token,"status_code":200,"user":user}

    return {"access_token": token, "token_type": "bearer"}
def registrer_user(email:str,password:str,name:str):
    with SessionLocal() as session:
        if session.query(Users).filter(Users.email==email).first():
            raise Exception("Usuario ya registrado")

        user = Users(
            email = email,
            hashed_password = hash_password(password),
            name = name
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"message": "Usuario creado","status_code":202}

        
