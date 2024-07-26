from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


# TODO: Needed?
# class UserInDB(UserBase):
#     hashed_password: str


class User(UserBase):
    id: int
    is_active: bool
    is_admin: Optional[bool] = None

    class ConfigDict:
        from_attributes = True


class UserStateUpdate(BaseModel):
    new_state: bool
