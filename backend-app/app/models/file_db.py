from sqlalchemy import Column, Integer, text
from app.sql_db.file_database import Base_file_db
from app.models.db_utils import map_dtype
import logging

logger = logging.getLogger(__name__)

def create_file_table_class(df, table_name, existing_columns=None, only_new_columns=False):
    columns = {
        '__tablename__': table_name,
        '__table_args__': {"extend_existing": True},
        'id': Column(Integer, primary_key=True, autoincrement=True)
    }
    
    for column_name, dtype in df.dtypes.items():
        if only_new_columns:
            if column_name not in existing_columns:
                columns[column_name] = Column(map_dtype(dtype))
        else:
            columns[column_name] = Column(map_dtype(dtype))
    
    if existing_columns and not only_new_columns:
        for column_name, column_type in existing_columns.items():
            if column_name != "id":  # Skip id as it's already defined
                columns[column_name] = Column(column_type)
    
    logger.info(f"Columns for {table_name}: {columns}")
    FileTable = type('FileTable', (Base_file_db,), columns)
    return FileTable

def update_schema(df, engine, metadata, table_name):
    metadata.reflect(bind=engine)
    table = metadata.tables.get(table_name)
    existing_columns = {col.name: col.type for col in table.columns}

    columns_to_add = []
    for column_name, dtype in df.dtypes.items():
        if column_name not in existing_columns:
            columns_to_add.append(Column(column_name, map_dtype(dtype)))
    
    if columns_to_add:
        with engine.connect() as conn:
            for column in columns_to_add:
                alter_stmt = text(
                    f'ALTER TABLE {table_name} ADD COLUMN "{column.name}" {column.type}'
                )
                logger.info(f"Executing: {alter_stmt}")
                conn.execute(alter_stmt)
                conn.commit()
            logger.info("Table updated")

    metadata.clear()
    metadata.reflect(bind=engine)
    existing_columns = {col.name: col.type for col in table.columns}
        
    FileTable = create_file_table_class(df, table_name, existing_columns=existing_columns)
    return FileTable
