from typing import Annotated, List

from fastapi import APIRouter, Depends

from db.models import Drink, User
from dependencies import get_current_user
from models import DrinkSchema
from utils import CamelModel

router = APIRouter(
    prefix='/drinks'
)


@router.get('/', response_model=List[DrinkSchema])
async def get_drinks(user: Annotated[User, Depends(get_current_user)]):
    foods = Drink.all()

    return await DrinkSchema.from_queryset(foods)


class DrinkSchemaIn(CamelModel):
    name: str

@router.post('/', response_model=DrinkSchema)
async def create_drink(drink: DrinkSchemaIn, user: Annotated[User, Depends(get_current_user)]):
    drink_obj = await Drink.create(**drink.model_dump(exclude_unset=True))

    return await DrinkSchema.from_tortoise_orm(drink_obj)
