
import datetime
from datetime import timedelta

from fastapi import APIRouter, HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr, Field

from config import settings
from db.models import User
from models import UserSchema
from utils import CamelModel

router = APIRouter(
    prefix='/sessions'
)


class SignInSchema(CamelModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=254, unique=True)
    password: str


@router.post('/sign-up', response_model=UserSchema)
async def sign_up(data: SignInSchema):
    if settings.IS_SIGN_UP_DISABLED:
        raise HTTPException(status_code=423, detail='Sign up is disabled')
    crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    data.password = crypt_context.hash(data.password)
    user = await User.create(**data.model_dump(exclude_unset=True))

    return await UserSchema.from_tortoise_orm(user)


class SignInResponseSchema(CamelModel):
    token: str


class SignInRequestSchema(CamelModel):
    email: EmailStr = Field(..., max_length=254)
    password: str


@router.post('/sign-in', response_model=SignInResponseSchema)
async def sign_in(data: SignInRequestSchema):
    user = await User.get_or_none(email=data.email)
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid email or password')
    crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    if not crypt_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    to_encode = {'sub': user.id, 'exp': datetime.utcnow() + timedelta(days=30)}
    return SignInResponseSchema(token=jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256'))
