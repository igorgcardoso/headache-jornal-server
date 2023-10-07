from typing import Annotated, List

from fastapi import APIRouter, Depends

from db.models import Remedy, User
from dependencies import get_current_user
from models import RemedySchema
from utils import CamelModel

router = APIRouter(
    prefix='/remedies'
)


@router.get('/', response_model=List[RemedySchema])
async def get_remedies(user: Annotated[User, Depends(get_current_user)]):
    remedies = Remedy.all()

    return await RemedySchema.from_queryset(remedies)


class RemedySchemaIn(CamelModel):
    name: str


@router.post('/', response_model=RemedySchema)
async def create_remedy(remedy: RemedySchemaIn, user: Annotated[User, Depends(get_current_user)]):
    remedy_obj = await Remedy.create(**remedy.model_dump(exclude_unset=True))

    return await RemedySchema.from_tortoise_orm(remedy_obj)
