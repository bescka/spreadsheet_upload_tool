from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from sqlalchemy.orm import Session
from app.models.user import User
from app.api.auth import get_current_active_user
from app.sql_db.file_crud import get_db
from app.models import file_db


router = APIRouter(tags=["fileupload"])


@router.post("/fileupload/", response_model=User)
# WARNING: Naming?
async def create_upload_file(
    file: UploadFile,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        engine = db.get_bind().engine
        print(engine.name)
        if file.filename.split(".")[-1] == "csv":  # WARNING: create check_file_type functin?
            # TODO: used with sanatization
            # schema_check = {
            #     "static_cols_names": {"name": str, "email": str, "id": pd.Int64Dtype},
            #     "static_cols_number": 3,
            #     "dynamic_col_dtype": {"other": pd.Int64Dtype},
            # }

            df = pd.read_csv(file.file)

            filetable = file_db.create_update_table(df, engine, "file_table")
            file_db.insert_data(db, df, filetable)
            return JSONResponse([df.to_json()])
        else:
            raise HTTPException(status_code=422, detail="File needs to have .csv format.")
    except Exception as e:
        raise e
