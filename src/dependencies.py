from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from config import settings
from db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='sessions/sign-in')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = await User.get_or_none(id=payload.get('sub'))
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user
