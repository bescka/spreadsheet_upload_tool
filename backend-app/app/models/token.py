from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

class TokenData(BaseModel):
    email: str
