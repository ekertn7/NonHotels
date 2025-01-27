"""Router for users"""

from fastapi import APIRouter, Response, Depends

from config import settings
from app.users.schemas import UsersRegisterSchema, UsersLoginSchema, UsersSchema
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.auth import get_hashed_password, authenticate_user, create_access_token
from app.users.dependencies import get_current_user

from app.exceptions.authentication_exceptions import UserAlreadyExistsException


router = APIRouter(
    prefix='/authenticate',
    tags=['Аутентификация'],
)


@router.post('/register')
async def register_user(user_data: UsersRegisterSchema):
    """Adds new user into database"""
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user is not None:
        raise UserAlreadyExistsException

    hashed_password = get_hashed_password(user_data.plain_password)

    await UsersDAO.insert(
        first_name=user_data.first_name,
        second_name=user_data.second_name,
        middle_name=user_data.middle_name,
        birth=user_data.birth,
        email=user_data.email,
        hashed_password=hashed_password)

    return {'result': 'successful registered'}


@router.post('/login')
async def login_user(response: Response, undefined_user_data: UsersLoginSchema):
    """Adds cookie with user token to browser"""
    authorised_user_data = await authenticate_user(
        user_email=undefined_user_data.email,
        user_plain_password=undefined_user_data.plain_password)

    jwt_token, jwt_expires = create_access_token(token_subject=authorised_user_data.id)

    response.set_cookie(
        settings.token_name, jwt_token, httponly=True, expires=jwt_expires,
        secure=False)

    return {
        'result': 'successful logged in',
        'user_id': authorised_user_data.id,
        'jwt_token': jwt_token}


@router.post('/logout')
async def logout_user(response: Response):
    """Removes cookie from browser"""
    response.delete_cookie(settings.token_name)
    return {'result': 'successful logged out'}


@router.get('/homepage')
async def get_user_info(user: Users = Depends(get_current_user)) -> UsersSchema:
    """Returns user info"""
    return user
