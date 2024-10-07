import logging

from app.sql_db import file_crud


# Test get_db
def test_get_db(db):
    session = db

    gen = file_crud.get_db()
    db = next(gen)

    try:
        assert type(db).__name__ == type(session).__name__

    finally:
        gen.close()


def test_create_update_table_new_table(df_files_good, db_engine, caplog):
    with caplog.at_level(logging.INFO):
        filetable, msg = file_crud.create_update_table(df_files_good, db_engine, "file_table")
        assert "Creating new table 'file_table'." in caplog.text
        assert msg == "Table with name file_table created"
        assert filetable.__tablename__ == "file_table"


def test_creat_update_table_existing_table(df_files_good, db_engine, caplog):
    with caplog.at_level(logging.INFO):
        filetable, msg = file_crud.create_update_table(df_files_good, db_engine, "file_table")
        assert "Table 'file_table' already exists. Using existing schema." in caplog.text
        assert msg == "Table with name file_table updated"
        assert filetable.__tablename__ == "file_table"


def test_insert_data_new_table(db, df_files_good, file_table_good, caplog):
    with caplog.at_level(logging.INFO):
        file_crud.insert_data(db, df_files_good, file_table_good)
        assert "Data inserted into file_table" in caplog.text.strip()
