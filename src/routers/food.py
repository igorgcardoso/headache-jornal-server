from typing import Annotated, List

from fastapi import APIRouter, Depends

from db.models import Food, User
from dependencies import get_current_user
from models import FoodSchema
from utils import CamelModel

router = APIRouter(
    prefix='/foods'
)


@router.get('/', response_model=List[FoodSchema])
async def get_foods(user: Annotated[User, Depends(get_current_user)]):
    foods = Food.all()

    return await FoodSchema.from_queryset(foods)


class FoodSchemaIn(CamelModel):
    name: str

@router.post('/')
async def create_food(food: FoodSchemaIn, user: Annotated[User, Depends(get_current_user)]):
    food_obj = await Food.create(**food.model_dump(exclude_unset=True))

    return await FoodSchema.from_tortoise_orm(food_obj)
