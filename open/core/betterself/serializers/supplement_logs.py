from rest_framework.fields import (
    UUIDField,
    HiddenField,
    CurrentUserDefault,
    CharField,
    DecimalField,
    ChoiceField,
)
from rest_framework.serializers import ModelSerializer

from open.core.betterself.constants import INPUT_SOURCES_TUPLES
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.serializers.simple_generic import create_name_uuid_serializer


class SupplementLogReadSerializer(ModelSerializer):
    supplement = create_name_uuid_serializer(Supplement)

    class Meta:
        model = SupplementLog
        fields = (
            "uuid",
            "notes",
            "created",
            "modified" "supplement",
            "source",
            "quantity",
            "time",
        )


class SupplementLogCreateUpdateSerializer(ModelSerializer):
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
    quantity = DecimalField(default=1)
    source = ChoiceField(INPUT_SOURCES_TUPLES)

    class Meta:
        model = SupplementLog
        fields = (
            "uuid",
            "created",
            "modified" "notes",
            "supplement",
            "source",
            "quantity",
            "time",
        )

    def validate(self, validated_data):
        user = self.context["request"].user

        if "supplement_uuid" in validated_data:
            supplement_uuid = validated_data.pop("supplement_uuid")
            supplement = Supplement.objects.get(uuid=supplement_uuid, user=user)
            validated_data["supplement"] = supplement

        return validated_data
