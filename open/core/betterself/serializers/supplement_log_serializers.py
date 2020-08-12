from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    UUIDField,
    HiddenField,
    CurrentUserDefault,
    CharField,
    DecimalField,
    ChoiceField,
)

from open.core.betterself.constants import INPUT_SOURCES_TUPLES, WEB_INPUT_SOURCE
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.simple_generic_serializer import (
    create_name_uuid_serializer,
)
from open.core.betterself.serializers.validators import validate_model_uuid
from open.utilities.date_and_time import get_utc_now


class SupplementLogReadSerializer(BaseModelReadSerializer):
    supplement = create_name_uuid_serializer(Supplement)

    class Meta:
        model = SupplementLog
        fields = (
            "display_name",
            "uuid",
            "notes",
            "created",
            "modified",
            "supplement",
            "source",
            "quantity",
            "time",
            "display_name",
        )

    def get_display_name(self, instance):
        # a janky way to always serialize a display name that sort of explains the instance
        time_ago = (get_utc_now() - instance.time).total_seconds()
        hours_ago = time_ago / 3600

        if hours_ago > 48:
            days_ago = hours_ago / 24
            relative_period_label = f"{days_ago:.01f} days ago"
        else:
            relative_period_label = f"{hours_ago:.01f} hours ago"

        name = f"{instance.quantity:.0f} x {instance.supplement.name} from {relative_period_label}"
        return name


class SupplementLogCreateUpdateSerializer(BaseCreateUpdateSerializer):
    supplement_uuid = UUIDField(source="supplement.uuid")
    user = HiddenField(default=CurrentUserDefault())
    uuid = UUIDField(required=False, read_only=True)
    notes = CharField(
        default="", trim_whitespace=True, required=False, allow_blank=True,
    )
    quantity = DecimalField(decimal_places=4, max_digits=10, default=1)
    source = ChoiceField(INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)

    class Meta:
        model = SupplementLog
        fields = (
            "user",
            "uuid",
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
