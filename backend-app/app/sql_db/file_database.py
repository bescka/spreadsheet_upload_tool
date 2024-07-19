import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("FILE_DB_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },  # WARNING:'check_same_thread only sqllite remove late
)
SessionLocalFileDb = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base_file_db = declarative_base()
