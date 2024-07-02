from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from app.models.user import User
from app.api.auth import get_current_active_user

router = APIRouter(tags=["fileupload"])


@router.post("/fileupload/", response_model=User)
# WARNING: Naming?
async def create_upload_file(
    file: UploadFile, current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        if file.filename.split(".")[-1] == "csv":  # WARNING: create check_file_type functin?
            df = pd.read_csv(file.file)
            # df = pd.melt(df, id_vars=['name', 'email', 'id'], var_name='date', value_name='value')
            return JSONResponse(df.to_json())
        else:
            raise HTTPException(status_code=422, detail="File needs to have .csv format.")
    except Exception as e:
        raise e
