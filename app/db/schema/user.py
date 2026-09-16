from pydantic import EmailStr,BaseModel
from typing import Union

class UserInCreate(BaseModel):
    email: EmailStr
    password: str

class UserOutput(BaseModel):
    id: int
    email: EmailStr

class UserInUpdate(BaseModel):
    id: int
    email: Union[EmailStr,None] = None
    password: Union[str,None] = None

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token: str