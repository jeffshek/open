from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    UUIDField,
    HiddenField,
    CurrentUserDefault,
    CharField,
    DecimalField,
    ChoiceField,
)
from rest_framework.serializers import ModelSerializer

from open.core.betterself.constants import INPUT_SOURCES_TUPLES, WEB_INPUT_SOURCE
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.serializers.mixins import BaseCreateUpdateSerializer
from open.core.betterself.serializers.simple_generic import create_name_uuid_serializer
from open.core.betterself.serializers.validators import validate_model_uuid


class SupplementLogReadSerializer(ModelSerializer):
    supplement = create_name_uuid_serializer(Supplement)

    class Meta:
        model = SupplementLog
        fields = (
            "uuid",
            "notes",
            "created",
            "modified",
            "supplement",
            "source",
            "quantity",
            "time",
        )


class SupplementLogCreateUpdateSerializer(BaseCreateUpdateSerializer):
    supplement_uuid = UUIDField(source="supplement.uuid")
    user = HiddenField(default=CurrentUserDefault())
    uuid = UUIDField(required=False, read_only=True)
    notes = CharField(
        default="",
        max_length=3000,
        trim_whitespace=True,
        required=False,
        allow_blank=True,
    )
    quantity = DecimalField(decimal_places=4, max_digits=10, default=1)
    source = ChoiceField(INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)

    class Meta:
        model = SupplementLog
        fields = (
            "user",
            "uuid",
            "created",
            "modified",
            "notes",
            "supplement_uuid",
            "source",
            "quantity",
            "time",
        )

    def validate_supplement_uuid(self, value):
        user = self.context["request"].user
        validate_model_uuid(Supplement, uuid=value, user=user)
        return value

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if validated_data.get("supplement"):
            supplement_uuid = validated_data["supplement"]["uuid"]
            supplement = Supplement.objects.get(uuid=supplement_uuid, user=user)
            validated_data["supplement"] = supplement

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user, supplement=supplement, time=validated_data["time"],
            ).exists():
                raise ValidationError(
                    f"Fields user, supplement, and time are not unique!"
                )

        return validated_data
