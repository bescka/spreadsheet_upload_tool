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
    # TODO: handel if table not updated
    metadata = MetaData()
    metadata.reflect(engine)
    if (len(Base_file_db.metadata.tables) == 0) & (len(metadata.tables) == 0):
        # change to log
        print(f"Creating new table '{table_name}'.")
        FileTable = create_file_table_class(df)
        Base_file_db.metadata.create_all(engine)
        return FileTable, f"Table with name {table_name} created"
    else:
        if table_name in metadata.tables:
            # change to log
            print(f"Table '{table_name}' already exists. Using existing schema.")
            FileTable = update_schema(df, engine, metadata, table_name)
            return FileTable, f"Table with name {table_name} updated"
        else:
            FileTable = create_file_table_class(df)
            Base_file_db.metadata.create_all(engine)
            # change to log
            print(f"Creating new table '{table_name}'.")
            return FileTable, f"Table with name {table_name} created"


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
