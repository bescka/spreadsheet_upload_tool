from app.sql_db.file_database import SessionLocalFileDb


def get_db():
    db = SessionLocalFileDb()
    try:
        yield db
    finally:
        db.close()
