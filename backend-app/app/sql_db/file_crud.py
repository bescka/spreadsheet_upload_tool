from app.sql_db.file_database import SessionLocalFileDb, Base_file_db
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
import pandas as pd
from app.models.file_db import create_file_table_class, update_schema
import logging

logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocalFileDb()
    try:
        yield db
    finally:
        db.close()

def create_update_table(df, engine, table_name):
    metadata = MetaData()
    metadata.reflect(engine)
    if table_name not in metadata.tables:
        logger.info(f"Creating new table '{table_name}'.")
        FileTable = create_file_table_class(df, table_name)
        Base_file_db.metadata.create_all(engine)
        return FileTable, f"Table with name {table_name} created"
    else:
        logger.info(f"Table '{table_name}' already exists. Using existing schema.")
        FileTable = update_schema(df, engine, metadata, table_name)
        metadata.clear()
        metadata.reflect(bind=engine)
        return FileTable, f"Table with name {table_name} updated"

def insert_data(db: Session, df: pd.DataFrame, FileTable, update_column_name="id"):
    # Ensure all numeric columns are correctly cast to numeric types
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Ensure all string columns are correctly cast to string types
    string_cols = df.select_dtypes(include=['object']).columns
    df[string_cols] = df[string_cols].astype(str)

    data = df.to_dict(orient="records")
    row_index = 1
    for record in data:
        existing_row = (
            db.query(FileTable)
            .filter(FileTable.__table__.columns[update_column_name] == row_index)
            .first()
        )

        if existing_row:
            for key, value in record.items():
                setattr(existing_row, key, value)
        else:
            new_row = FileTable(**record)
            db.add(new_row)
        row_index += 1
    db.commit()
    logger.info(f"Data inserted into {FileTable.__tablename__}")
