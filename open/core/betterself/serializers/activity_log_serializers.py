from rest_framework.exceptions import ValidationError
from rest_framework.fields import UUIDField

from open.core.betterself.models.activity import Activity
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.simple_generic_serializer import (
    create_name_uuid_serializer,
)
from open.core.betterself.serializers.validators import ModelValidatorsMixin


class ActivityLogReadSerializer(BaseModelReadSerializer):
    activity = create_name_uuid_serializer(Activity)

    class Meta:
        model = ActivityLog
        fields = (
            "uuid",
            "activity",
            "source",
            "duration_minutes",
            "time",
            "notes",
            # "created",
            # "modified",
            "display_name",
        )


class ActivityLogCreateUpdateSerializer(
    BaseCreateUpdateSerializer, ModelValidatorsMixin
):
    activity_uuid = UUIDField(source="activity.uuid")

    class Meta:
        model = ActivityLog
        fields = (
            "activity_uuid",
            "source",
            "duration_minutes",
            "time",
            "notes",
            "user",
        )

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if validated_data.get("activity"):
            activity_uuid = validated_data.pop("activity")["uuid"]
            activity = Activity.objects.get(uuid=activity_uuid, user=user)
            validated_data["activity"] = activity

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user, activity=activity, time=validated_data["time"],
            ).exists():
                raise ValidationError(
                    f"Fields user, ingredient, measurement, and quantity are not unique!"
                )

        return validated_data
