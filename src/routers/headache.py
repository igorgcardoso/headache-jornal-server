from typing import Annotated, List, Optional

import pendulum
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import Field
from tortoise.transactions import atomic

from db.enums import HeadacheIntensity, HeadacheSide, RemedyResult
from db.models import (Drink, Food, Headache, HeadacheRemedy, Remedy, User,
                       Weather)
from dependencies import get_current_user
from models import (DrinkSchema, FoodSchema, HeadacheRemedySchema,
                    HeadacheSchema, RemedySchema)
from utils import CamelModel, get_weather

router = APIRouter(
    prefix='/headaches'
)

class HeadacheSchemaIn(CamelModel):
    start_timestamp: str
    end_timestamp: Optional[str] = None
    intensity: HeadacheIntensity
    side: HeadacheSide
    pressure_or_squeezing: bool
    throbbing_or_pulsating: bool
    stabbing: bool
    nausea_vomiting: bool
    light_sensitivity: bool
    noise_sensitivity: bool
    sleep_rank: int


@router.get('/', response_model=List[HeadacheSchema])
async def get_headaches(user: Annotated[User, Depends(get_current_user)]):
    headaches = Headache.all()

    return await HeadacheSchema.from_queryset(headaches)

class HeadacheRemedySchemaOut(HeadacheRemedySchema):
    remedy: RemedySchema

class HeadacheDetails(HeadacheSchema):
    foods: List[FoodSchema]
    drinks: List[DrinkSchema]
    remedies: List[HeadacheRemedySchemaOut]


@router.get('/{id}', response_model=HeadacheDetails)
async def get_headache(id: str, user: Annotated[User, Depends(get_current_user)]):
    headache = Headache.get(id=id)

    headache = await headache.prefetch_related('foods', 'drinks', 'remedies__remedy', 'remedies', 'weather')

    headache_log = await HeadacheDetails.from_tortoise_orm(headache)

    return headache_log


@router.post('/', response_model=HeadacheSchema)
@atomic()
async def add_headache(headache: HeadacheSchemaIn, latitude: Annotated[float, Query()], longitude: Annotated[float, Query()], user: Annotated[User, Depends(get_current_user)]):
    data = headache.model_dump(exclude_unset=True)

    weather_data = await get_weather(latitude, longitude)

    weather = await Weather.create(
        min_temperature=weather_data.temperature_2m_min[0],
        max_temperature=weather_data.temperature_2m_max[0],
        apparent_min_temperature=weather_data.apparent_temperature_min[0],
        apparent_max_temperature=weather_data.apparent_temperature_max[0],
        uv_index=weather_data.uv_index_max[0],
        shortwave_radiation=weather_data.shortwave_radiation_sum[0],
        temperature=weather_data.temperature_2m[0],
        apparent_temperature=weather_data.apparent_temperature[0],
    )

    headache_obj = await Headache.create(**data, weather=weather, user=user)

    return await HeadacheSchema.from_tortoise_orm(headache_obj)


@router.get('/unended', response_model=List[HeadacheSchema])
async def get_unended_headaches(user: Annotated[User, Depends(get_current_user)]):
    headaches = Headache.filter(end_timestamp=None)

    return await HeadacheSchema.from_queryset(headaches)


@router.patch('/{id}', response_model=HeadacheSchema)
async def end_headache(id: str, user: Annotated[User, Depends(get_current_user)]):
    headache = await Headache.get(id=id)
    if headache.end_timestamp is not None:
        raise HTTPException(status_code=403, detail='Headache already ended')
    headache.end_timestamp = pendulum.now()
    await headache.save()

    return await HeadacheSchema.from_tortoise_orm(headache)


@router.patch('/{id}/foods-and-drinks', response_model=HeadacheSchema)
async def add_foods_and_drinks(id: str, foods: List[str], drinks: List[str], user: Annotated[User, Depends(get_current_user)]):
    headache = await Headache.get(id=id)

    foods = await Food.filter(id__in=foods)
    drinks = await Drink.filter(id__in=drinks)

    await headache.foods.add(*foods)
    await headache.drinks.add(*drinks)

    await headache.save()

    return await HeadacheSchema.from_tortoise_orm(headache)


class HeadacheRemedySchemaIn(CamelModel):
    id: str
    quantity: int = Field(..., gt=1)


@router.patch('/{id}/remedies', response_model=HeadacheSchema)
@atomic()
async def add_remedies(id: str, remedy: HeadacheRemedySchemaIn, user: Annotated[User, Depends(get_current_user)]):
    headache = await Headache.get(id=id)
    remedy_model = await Remedy.get(id=remedy.id)

    try:
        headache_remedy = await HeadacheRemedy.get(remedy=remedy_model, headache=headache)
        headache_remedy.quantity += remedy.quantity
        await headache_remedy.save()
    except HeadacheRemedy.DoesNotExist:
        headache_remedy = await HeadacheRemedy.create(remedy=remedy_model, quantity=remedy.quantity, headache=headache)

    return await HeadacheSchema.from_tortoise_orm(headache)


class HeadacheRemedyResultSchema(CamelModel):
    result: str

@router.patch('/{id}/remedies/{remedy_id}/result', response_model=HeadacheSchema)
async def set_remedy_result(id: str, remedy_id: str, body: HeadacheRemedyResultSchema, user: Annotated[User, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=401, detail='Unauthorized')
    headache_remedy = await HeadacheRemedy.get(id=remedy_id, headache_id=id)
    if headache_remedy.result != RemedyResult.NO_EFFECT:
        raise HTTPException(status_code=403, detail='Result already set')

    result = body.result

    try:
        result = RemedyResult(result)
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid result')

    headache_remedy.result = result
    await headache_remedy.save()

    headache = await Headache.get(id=id)

    return await HeadacheSchema.from_tortoise_orm(headache)

