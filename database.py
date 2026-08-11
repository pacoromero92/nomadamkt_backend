from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
DB_STRING = os.getenv('DB_STRING')
Base = declarative_base()
engine = create_engine(DB_STRING)
SessionLocal = sessionmaker(bind=engine)