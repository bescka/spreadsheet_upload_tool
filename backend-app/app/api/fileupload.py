from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from sqlalchemy.orm import Session
from app.models.user import User
from app.api.auth import get_current_active_user
from app.sql_db.file_crud import get_db, create_update_table, insert_data
import logging

router = APIRouter(tags=["fileupload"])

@router.post("/fileupload/", response_model=User)
async def create_upload_file(
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        engine = db.get_bind().engine
        logging.info(f"Database engine: {engine.name}")
        if file.filename.split(".")[-1] == "csv":
            df = pd.read_csv(file.file)
            logging.info(f"DataFrame loaded: {df.head()}")
            filetable, msg = create_update_table(df, engine, "file_table")
            logging.info(f"Table creation/update message: {msg}")
            insert_data(db, df, filetable)
            return JSONResponse({"message": msg})
        else:
            raise HTTPException(status_code=422, detail="File needs to have .csv format.")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
