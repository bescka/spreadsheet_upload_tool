from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from app.models.user import User
from app.api.auth import get_current_active_user

router = APIRouter(
    tags=['fileupload']
)

@router.post('/fileupload/', response_model=User)
async def create_upload_file(file: UploadFile, current_user: Annotated[User,  Depends(get_current_active_user)]):
    # TODO: use CSV, 
    # TODO: catch wrong content 
    # 
    try:
        if file.filename.split('.')[-1] == 'xlsx': # WARNING: create check_file_type functin?
            df = pd.read_excel(file.file)
            # df = pd.melt(df, id_vars=['name', 'email', 'id'], var_name='date', value_name='value')
            return JSONResponse(df.head().to_json())
        else:
            raise HTTPException(status_code=422, detail='File needs to have .xlsx format.')
    except Exception as e:
        raise e
