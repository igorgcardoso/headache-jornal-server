from typing import Any, Dict, List

import httpx
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class WeatherSchema(BaseModel):
    temperature_2m_max: List[float]
    temperature_2m_min: List[float]
    apparent_temperature_max: List[float]
    apparent_temperature_min: List[float]
    uv_index_max: List[float]
    shortwave_radiation_sum: List[float]
    temperature_2m: List[float]
    apparent_temperature: List[float]

async def get_weather(latitude: float, longitude: float) -> WeatherSchema:
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,apparent_temperature&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,uv_index_max,shortwave_radiation_sum&timezone=America%2FSao_Paulo&forecast_days=1')
        json = response.json()
        daily: Dict[str, Any] = json.pop('daily')
        hourly: Dict[str, Any] = json.pop('hourly')
    for key in list(daily.keys()):
        if key not in WeatherSchema.__fields__:
            del daily[key]
    for key in list(hourly.keys()):
        if key not in WeatherSchema.__fields__:
            del hourly[key]

    weather_data = WeatherSchema(**daily, **hourly)
    return weather_data


model_config = ConfigDict(
        alias_generator = to_camel,
        populate_by_name = True,
    )

class CamelModel(BaseModel):
    model_config = model_config
