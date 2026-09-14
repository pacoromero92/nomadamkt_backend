from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from auth.utils import hash_password
from models.Role import Role
db: Session = SessionLocal()

user = Users(
    email="pacoromero92@outlook.com",
    hashed_password=hash_password("TuPassword123"),
    name="Frencisco",
    role=Role.ADMIN,
    is_active=True,
    is_verified=True
)

db.add(user)
db.commit()
db.refresh(user)

print(f"Usuario creado: {user.email}")

db.close()