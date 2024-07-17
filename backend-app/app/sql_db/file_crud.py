from app.sql_db.file_database import SessionLocalFileDb


def get_db():
    db = SessionLocalFileDb()
    try:
        yield db
    finally:
        db.close()


def get_file_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={
            "check_same_thread": False
        },  # WARNING:'check_same_thread only sqllite remove late
    )
    return engine
