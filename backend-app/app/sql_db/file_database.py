import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("FILE_DB_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
SessionLocalFileDb = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base_file_db = declarative_base()
