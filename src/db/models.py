from uuid import uuid4

import pendulum
from tortoise import fields
from tortoise.models import Model
from tortoise.validators import MinValueValidator

from db.enums import HeadacheIntensity, HeadacheSide, RemedyResult


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=254, unique=True)
    password = fields.CharField(max_length=255)


class Food(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    name = fields.CharField(max_length=50)


class Drink(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    name = fields.CharField(max_length=50)


class Remedy(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    name = fields.CharField(max_length=50)


class HeadacheRemedy(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    headache = fields.ForeignKeyField('models.Headache', related_name='remedies')
    remedy = fields.ForeignKeyField('models.Remedy', related_name=None)
    quantity = fields.IntField(validators=[MinValueValidator(1)])
    result = fields.CharEnumField(enum_type=RemedyResult, default=RemedyResult.NO_EFFECT)
    taken_timestamp = fields.DatetimeField(auto_now_add=True)


class Weather(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    min_temperature = fields.IntField()
    max_temperature = fields.IntField()
    apparent_min_temperature = fields.IntField()
    apparent_max_temperature = fields.IntField()
    uv_index = fields.IntField()
    shortwave_radiation = fields.IntField()
    temperature = fields.IntField()
    apparent_temperature = fields.IntField()


class Headache(Model):
    id = fields.UUIDField(pk=True, default=uuid4)
    user = fields.ForeignKeyField('models.User', related_name=None)
    start_timestamp = fields.DatetimeField(auto_now_add=True)
    end_timestamp = fields.DatetimeField(null=True)
    intensity = fields.IntEnumField(enum_type=HeadacheIntensity)
    side = fields.CharEnumField(enum_type=HeadacheSide)
    pressure_or_squeezing = fields.BooleanField()
    throbbing_or_pulsating = fields.BooleanField()
    stabbing = fields.BooleanField()
    nausea_vomiting = fields.BooleanField()
    light_sensitivity = fields.BooleanField()
    noise_sensitivity = fields.BooleanField()
    foods = fields.ManyToManyField('models.Food', related_name=None)
    drinks = fields.ManyToManyField('models.Drink', related_name=None)
    sleep_rank = fields.IntField(constraints={"ge": 1, "le": 100})
    weather = fields.ForeignKeyField('models.Weather', related_name=None)
    remedies: fields.ReverseRelation['HeadacheRemedy']

    def duration_in_seconds(self) -> int:
        if self.end_timestamp is None:
            return pendulum.now().diff(self.start_timestamp).seconds
        return (self.end_timestamp - self.start_timestamp).seconds

    def intensity_name(self) -> str:
        return HeadacheIntensity(self.intensity).name

    class PydanticMeta:
        computed = ['duration_in_seconds', 'intensity_name']

    class Meta:
        ordering = ['-start_timestamp']
