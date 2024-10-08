# New imports security.py
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.token import Token, TokenData
from app.models.user import User
from app.sql_db.crud import get_db, get_user_by_email

load_dotenv()
SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
ALGORITHM = os.getenv("FASTAPI_HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticates a user using their email address and password."""
    try:
        user = get_user_by_email(db, email)
        if not verify_password(password, user.hashed_password):
            return False
        return user
    except Exception as e:
        print(f"Error occurred while authenticating user: {e}")
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")


async def get_current_active_admin(current_user: Annotated[User, Depends(get_current_user)]):
    if (current_user.is_active == True) & (current_user.is_admin == True):
        return current_user
    raise HTTPException(status_code=400, detail="Not Authorized!")


router = APIRouter()


@router.get("/")
async def api_health_check():
    return {"Status": "Something Different"}


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer", message="Welcome!")
