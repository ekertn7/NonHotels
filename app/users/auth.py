from datetime import datetime, timedelta, UTC

from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from pydantic import EmailStr

from config import settings
from app.users.dao import UsersDAO
from app.users.schemas import UsersSchema

from app.exceptions.authentication_exceptions import (
    WrongUserEmailException, WrongUserPasswordException)


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_plain_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        token_subject: str | int | float,
        token_secret: str = settings.token_secret,
        token_algorithm: str = settings.token_algorithm,
        token_lifetime: timedelta = settings.token_lifetime) -> str:
    token_data = {}

    token_data.update({'sub': str(token_subject)})

    expire_datetime = datetime.now(UTC) + token_lifetime
    token_data.update({'exp': expire_datetime})

    encoded_token = jwt.encode(token_data, token_secret, token_algorithm)

    return encoded_token, expire_datetime


async def authenticate_user(user_email: EmailStr, user_plain_password: str) -> UsersSchema:
    existing_user = await UsersDAO.find_one_or_none(email=user_email)
    if existing_user is None:
        raise WrongUserEmailException

    passwords_matching = verify_plain_password(
        user_plain_password, existing_user.hashed_password)

    if passwords_matching is False:
        raise WrongUserPasswordException

    return existing_user
