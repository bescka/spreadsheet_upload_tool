import logging
from typing import Annotated

import pandas as pd
from app.api.auth import get_current_active_user
from app.models.user import User
from app.sql_db.file_crud import create_update_table, get_db, insert_data
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

router = APIRouter(tags=["fileupload"])


@router.post("/fileupload/", response_model=User)
async def create_upload_file(
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        engine = db.get_bind().engine
        logger.info(f"Database engine: {engine.name}")
        if file.filename.split(".")[-1] == "csv":
            df = pd.read_csv(file.file)
            logger.info(f"DataFrame loaded: {df.head()}")
            filetable, msg = create_update_table(df, engine, "file_table")
            logger.info(f"Table creation/update message: {msg}")
            insert_data(db, df, filetable)
            return JSONResponse({"message": msg})
        else:
            raise HTTPException(status_code=422, detail="File needs to have .csv format.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return e
