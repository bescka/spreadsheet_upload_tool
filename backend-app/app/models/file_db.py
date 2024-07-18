from sqlalchemy import Column, Integer
from sqlalchemy import text
from app.sql_db.file_database import Base_file_db
from app.models.db_utils import map_dtype


def create_file_table_class(df, existing_columns=None, only_new_columns=False):
    class FileTable(Base_file_db):
        __tablename__ = "file_table"
        __table_args__ = {"extend_existing": "extend_existing"}
        # HACK: May change to use df index for id not autoincrement give id column
        # also name `id` could be as column in file, couses errror
        id = Column(Integer, primary_key=True, autoincrement=True)

        # Add columns based on the DataFrame
        for column_name, dtype in df.dtypes.items():
            if only_new_columns:
                if column_name not in existing_columns:
                    vars()[column_name] = Column(map_dtype(dtype))
            else:
                vars()[column_name] = Column(map_dtype(dtype))

        # Add existing columns if only_new_columns is False
        if existing_columns and not only_new_columns:
            for column_name, column_type in existing_columns.items():
                if column_name != "id":  # Skip id as it's already defined
                    vars()[column_name] = Column(column_type)

    return FileTable


def update_schema(df, engine, metadata, table_name):
    # TODO:
    # - print/log if table stays unchanged/ exception
    # - change alter_stmt to save option
    table = metadata.tables.get(table_name)
    existing_columns = {col.name: col.type for col in table.columns}

    columns_to_add = []
    for column_name, dtype in df.dtypes.items():
        if column_name not in existing_columns:
            columns_to_add.append(Column(column_name, map_dtype(dtype)))
    if columns_to_add:
        with engine.connect() as conn:
            # Use SQLAlchemy to generate ALTER TABLE statements %s syntax
            for column in columns_to_add:
                # HACK:
                # alter_stmt = table.append_column(column)
                alter_stmt = text(
                    f'ALTER TABLE file_table ADD COLUMN "{column.name}" {column.type}'
                )
                print(alter_stmt)
                conn.execute(alter_stmt)
            print("Table updated")
    FileTable = create_file_table_class(df, existing_columns=existing_columns)

    return FileTable
