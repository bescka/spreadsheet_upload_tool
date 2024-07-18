from app.sql_db.file_database import SessionLocalFileDb
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
import pandas as pd
from app.sql_db.file_database import Base_file_db
from app.models.file_db import create_file_table_class, update_schema


def get_db():
    db = SessionLocalFileDb()
    try:
        yield db
    finally:
        db.close()


def create_update_table(df, engine, table_name):
    metadata = MetaData()
    metadata.reflect(engine)
    if (len(Base_file_db.metadata.tables) == 0) & (len(metadata.tables) == 0):
        FileTable = create_file_table_class(df)
        Base_file_db.metadata.create_all(engine)
        print(f"Creating new table '{table_name}'.")
        return FileTable
    else:
        if table_name in metadata.tables:
            print(f"Table '{table_name}' already exists. Using existing schema.")
            return update_schema(df, engine, metadata, table_name)
        else:
            FileTable = create_file_table_class(df)
            Base_file_db.metadata.create_all(engine)
            print(f"Creating new table '{table_name}'.")
            return FileTable


def insert_data(db: Session, df: pd.DataFrame, FileTable, update_column_name="id"):
    data = df.to_dict(orient="records")
    # HACK:
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
