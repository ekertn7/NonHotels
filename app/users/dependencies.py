"""Dependencies for users authentication"""

from datetime import datetime
from jose import jwt, JWTError
from fastapi import Depends, Request

from config import settings
from app.users.models import Users
from app.users.dao import UsersDAO

from app.exceptions.authentication_exceptions import (
    TokenIsNotExistsException, TokenExpiredException,
    IncorrectTokenFormatException, IncorrectTokenDataException,
    UserIsNotExistsException)


def get_token(request: Request):
    """Getting token from cookies"""
    token = request.cookies.get(settings.token_name)
    if token is None:
        raise TokenIsNotExistsException
    return token


async def get_current_user(encoded_token: str = Depends(get_token)) -> Users:
    """Getting current user data from token"""
    try:
        token_payload = jwt.decode(
            encoded_token, settings.token_secret,
            settings.token_algorithm)
    except JWTError:
        raise IncorrectTokenFormatException from None

    token_expires: str = token_payload.get('exp')
    current_timestamp = int(round(datetime.utcnow().timestamp()))
    if token_expires is None or (int(token_expires) < current_timestamp):
        raise TokenExpiredException

    user_id: str = token_payload.get('sub')
    if user_id is None:
        raise IncorrectTokenDataException

    user = await UsersDAO.find_by_id(id=int(user_id))
    if user is None:
        raise UserIsNotExistsException

    return user
