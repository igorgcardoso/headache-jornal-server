from datetime import datetime
from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from tortoise.functions import Avg, Count

from db.enums import HeadacheIntensity, HeadacheSide, RemedyResult
from db.models import Headache, HeadacheRemedy, User
from dependencies import get_current_user
from utils import CamelModel

router = APIRouter(
    prefix='/stats'
)

class HeadacheStatsSchema(CamelModel):
    occurrences: int = 0
    mean_duration: float = 0.0
    mean_sleep_rank: float = 0.0
    most_common_intensity: Optional[HeadacheIntensity] = None
    most_common_intensity_name: Optional[str] = None
    mean_remedies: List[Dict[str, Any]] = []
    most_common_remedy_result: Optional[RemedyResult] = None
    weekday_histogram: List[Dict[str, int]] = []
    most_common_side: Optional[HeadacheSide] = None
    most_common_side_name: Optional[str] = None
    mean_temperature: Optional[float] = None
    mean_apparent_temperature: Optional[float] = None
    mean_uv_index: Optional[float] = None
    mean_shortwave_radiation: Optional[float] = None
    mean_min_temperature: Optional[float] = None
    mean_max_temperature: Optional[float] = None
    mean_apparent_min_temperature: Optional[float] = None
    mean_apparent_max_temperature: Optional[float] = None


@router.get('/', response_model=HeadacheStatsSchema)
async def stats(user: Annotated[User, Depends(get_current_user)], start_date: Annotated[datetime, Query()] = None, end_date: Annotated[datetime, Query()] = datetime.now()):
    if start_date is None:
        # headaches = HeadacheLog.filter(end_timestamp__lte=end_date)
        headaches = Headache.filter(start_timestamp__lte=end_date)
    else:
        headaches = Headache.filter(start_timestamp__gte=start_date, start_timestamp__lte=end_date)

    occurrences = len(await headaches)

    headaches = headaches.annotate(
        count_intensity=Count('intensity'),
        count_side=Count('side'),
        mean_temperature=Avg('weather__temperature'),
        mean_apparent_temperature=Avg('weather__apparent_temperature'),
        mean_uv_index=Avg('weather__uv_index'),
        mean_shortwave_radiation=Avg('weather__shortwave_radiation'),
        mean_min_temperature=Avg('weather__min_temperature'),
        mean_max_temperature=Avg('weather__max_temperature'),
        mean_apparent_min_temperature=Avg('weather__apparent_min_temperature'),
        mean_apparent_max_temperature=Avg('weather__apparent_max_temperature'),
        mean_sleep_rank=Avg('sleep_rank'),
    )

    if occurrences == 0:
        return HeadacheStatsSchema()

    most_common_intensity = await headaches.order_by('-count_intensity').first()
    most_common_intensity = most_common_intensity.intensity
    headaches_remedy = HeadacheRemedy.filter(headache__id__in=await headaches.values_list('id', flat=True))
    mean_remedies = await headaches_remedy.group_by('remedy__id').annotate(
        mean_quantity=Avg('quantity')
    ).values('remedy__name', 'mean_quantity')
    most_common_remedy_result = await headaches_remedy.group_by('result').annotate(
        count=Count('result')
    ).order_by('-count').first()
    most_common_side = await headaches.order_by('-count_side').first()
    headache = await headaches.first()

    return HeadacheStatsSchema(
        occurrences=occurrences,
        most_common_intensity=most_common_intensity,
        most_common_intensity_name=most_common_intensity.name,
        mean_remedies=[{'name': remedy.get('remedy__name', ''), 'mean_quantity': remedy.get('mean_quantity', 0)} for remedy in  mean_remedies],
        most_common_remedy_result=most_common_remedy_result.result if most_common_remedy_result else None,
        most_common_side=most_common_side.side,
        most_common_side_name=most_common_side.side.name,
        mean_temperature=headache.mean_temperature,
        mean_apparent_temperature=headache.mean_apparent_temperature,
        mean_uv_index=headache.mean_uv_index,
        mean_shortwave_radiation=headache.mean_shortwave_radiation,
        mean_min_temperature=headache.mean_min_temperature,
        mean_max_temperature=headache.mean_max_temperature,
        mean_apparent_min_temperature=headache.mean_apparent_min_temperature,
        mean_apparent_max_temperature=headache.mean_apparent_max_temperature,
        mean_sleep_rank=headache.mean_sleep_rank,
    )
