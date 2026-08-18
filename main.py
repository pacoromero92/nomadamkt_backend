import os
from database import Base, engine
from fastapi import FastAPI
from api.routes.insights import router as insights_router
from api.routes.auth import router as auth_router
from api.routes.clients import router as client_router
from api.routes.sync import router as services_router
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()

app.include_router(insights_router)
app.include_router(auth_router)
app.include_router(client_router)
app.include_router(services_router)
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
