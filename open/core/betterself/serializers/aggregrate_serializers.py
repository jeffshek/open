from rest_framework.fields import DateField, ListField, UUIDField
from rest_framework.serializers import Serializer

from open.core.betterself.models.activity import Activity
from open.core.betterself.models.food import Food
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.serializers.validators import (
    generic_model_uuid_validator,
)


class AggregrateViewParamsSerializer(Serializer):
    start_date = DateField()
    end_date = DateField()
    supplement_uuids = ListField(
        child=UUIDField(validators=[generic_model_uuid_validator(Supplement)]),
        required=False,
    )
    activity_uuids = ListField(
        child=UUIDField(validators=[generic_model_uuid_validator(Activity)]),
        required=False,
    )
    food_uuids = ListField(
        child=UUIDField(validators=[generic_model_uuid_validator(Food)]), required=False
    )

    class Meta:
        fields = (
            "start_date",
            "end_date",
            "supplement_uuids",
            "activity_uuids",
            "food_uuids",
        )
