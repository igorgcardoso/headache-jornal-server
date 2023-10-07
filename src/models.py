from tortoise.contrib.pydantic import pydantic_model_creator

from db.models import (Drink, Food, Headache, HeadacheRemedy, Remedy, User,
                       Weather)
from utils import model_config

UserSchema = pydantic_model_creator(User, name='User', model_config=model_config, exclude=('password',))
FoodSchema = pydantic_model_creator(Food, name='Food', model_config=model_config)
DrinkSchema = pydantic_model_creator(Drink, name='Drink', model_config=model_config)
RemedySchema = pydantic_model_creator(Remedy, name='Remedy', model_config=model_config)
HeadacheRemedySchema = pydantic_model_creator(HeadacheRemedy, name='HeadacheRemedy', model_config=model_config)
HeadacheSchema = pydantic_model_creator(Headache, name='HeadacheLog', model_config=model_config)
WeatherSchema = pydantic_model_creator(Weather, name='Weather', model_config=model_config)
