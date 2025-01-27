"""Authentication exceptions"""

from fastapi import HTTPException, status as status_codes


UserAlreadyExistsException = HTTPException(
    status_code=status_codes.HTTP_409_CONFLICT,
    detail='User already exists',)


WrongUserEmailException = HTTPException(
    status_code=status_codes.HTTP_401_UNAUTHORIZED,
    detail='Incorrect user email',)


WrongUserPasswordException = HTTPException(
    status_code=status_codes.HTTP_401_UNAUTHORIZED,
    detail='Incorrect user password',)


TokenIsNotExistsException = HTTPException(
    status_code=status_codes.HTTP_401_UNAUTHORIZED,
    detail='Token is not found',)


TokenExpiredException = HTTPException(
    status_code=status_codes.HTTP_401_UNAUTHORIZED,
    detail='Token expired',)


IncorrectTokenFormatException = HTTPException(
    status_code=status_codes.HTTP_401_UNAUTHORIZED,
    detail='Incorrect token format',)


IncorrectTokenDataException = HTTPException(
    status_code=status_codes.HTTP_401_UNAUTHORIZED,
    detail='Incorrect token data',)


UserIsNotExistsException = HTTPException(
    status_code=status_codes.HTTP_401_UNAUTHORIZED,
    detail='User is not exists',)
