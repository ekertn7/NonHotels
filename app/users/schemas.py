"""Schemas for users"""

from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr


class UsersSchema(BaseModel):
    id: int
    first_name: str
    second_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth: date
    email: EmailStr
    hashed_password: str

    # class Config:
    #     from_attributes = True  # orm_mode = True


class UsersRegisterSchema(BaseModel):
    first_name: str
    second_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth: date
    email: EmailStr
    plain_password: str


class UsersLoginSchema(BaseModel):
    email: EmailStr
    plain_password: str
