from rest_framework.exceptions import ValidationError

from open.core.betterself.models.activity import Activity
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)


class ActivityReadSerializer(BaseModelReadSerializer):
    class Meta:
        model = Activity
        fields = (
            "uuid",
            "name",
            "is_significant_activity",
            "is_negative_activity",
            "is_all_day_activity",
            "notes",
            "created",
            "modified",
            "display_name",
        )


class ActivityCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Activity
        fields = (
            "name",
            "is_significant_activity",
            "is_negative_activity",
            "is_all_day_activity",
            "notes",
            "user",
        )

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user, name=validated_data["name"],
            ).exists():
                raise ValidationError(f"Fields user and activity name are not unique!")

        return validated_data
