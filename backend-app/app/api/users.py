from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import app.models.database as models  # INFO: Naming?
import app.models.user as api_m
from app.api.auth import get_current_active_admin, get_current_active_user
from app.sql_db import crud
from app.sql_db.crud import get_db
from app.sql_db.database import engine


def init_db():
    print("creating db...")
    models.Base.metadata.create_all(bind=engine)
    print("db created")


router = APIRouter(
    prefix="/users",
    tags=["user"],
)

# TODO: change endpoint?


# No authentication
@router.post("/", response_model=api_m.User)
def create_user(user: api_m.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# User authentication
@router.get("/me/", response_model=api_m.User)
async def read_users_me(current_user: Annotated[api_m.User, Depends(get_current_active_user)]):
    return current_user


@router.put("/me/update_state/")
# TODO: Does this route make sence?
def update_user_state(
    new_state: api_m.UserStateUpdate,
    current_user: Annotated[api_m.User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    # WARNING: expection doesn't make sence
    # if current_user is None:
    #     raise HTTPException(status_code=404, detail=f"User not found")
    # TODO: improve exception handeling
    if current_user.is_active is new_state.new_state:
        raise HTTPException(
            status_code=404,
            detail=f"User is_active is set to {new_state.new_state} already!",
        )
    _ = crud.update_is_active(db, current_user, new_state.new_state)
    return JSONResponse(content={"Message": "User status updated"})


# Admin authentication
# TODO: change route
@router.get("/users/", response_model=list[api_m.User])
def read_users(
    current_user: Annotated[api_m.User, Depends(get_current_active_admin)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/id/{user_id}", response_model=api_m.User)
def read_user(
    user_id: int,
    current_user: Annotated[api_m.User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User not found")
    return db_user


@router.get("/mail/{user_mail}", response_model=api_m.User, tags=["user"])
def read_user_by_mail(
    user_mail: str,
    current_user: Annotated[api_m.User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_email(db, email=user_mail)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}/update_admin/", response_model=api_m.User)
def promote_to_admin(
    user_id: int,
    current_user: Annotated[api_m.User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User not found")
    # TODO: improve exception handeling
    if db_user.is_admin is None:
        updated_user = crud.update_is_admin(db, db_user)
        return updated_user
    else:
        raise HTTPException(status_code=404, detail=f"User is already admin")


# TODO: change name to update_state_by_id
@router.put("/{user_id}/update_state/")
def update_any_user_state(
    user_id: int,
    new_state: api_m.UserStateUpdate,
    current_user: Annotated[api_m.User, Depends(get_current_active_admin)],
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User not found")
    # TODO: improve exception handeling
    if db_user.is_active is new_state.new_state:
        raise HTTPException(
            status_code=404,
            detail=f"User is_active is set to {new_state.new_state} already!",
        )
    updated_user = crud.update_is_active(db, db_user, new_state.new_state)
    return JSONResponse(content={"Message": "User status updated"})
