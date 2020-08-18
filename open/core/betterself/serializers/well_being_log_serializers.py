from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField

from open.core.betterself.constants import INPUT_SOURCES_TUPLES, WEB_INPUT_SOURCE
from open.core.betterself.models.well_being_log import WellBeingLog
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.validators import ModelValidatorsMixin


class WellBeingLogReadSerializer(BaseModelReadSerializer):
    class Meta:
        model = WellBeingLog
        fields = (
            "mental_value",
            "physical_value",
            "time",
            "source",
            "notes",
            # "created",
            # "modified",
            "uuid",
            "display_name",
        )


class WellBeingLogCreateUpdateSerializer(
    BaseCreateUpdateSerializer, ModelValidatorsMixin
):
    source = ChoiceField(INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)

    class Meta:
        model = WellBeingLog
        fields = (
            "mental_value",
            "physical_value",
            "time",
            "source",
            "notes",
            "user",
        )

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user, time=validated_data["time"],
            ).exists():
                raise ValidationError(f"Fields user and time are not unique!")

        return validated_data
