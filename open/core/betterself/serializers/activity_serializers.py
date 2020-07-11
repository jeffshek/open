from rest_framework.serializers import ModelSerializer

from open.core.betterself.models.activity import Activity
from open.core.betterself.serializers.mixins import BaseCreateUpdateSerializer


class ActivityReadSerializer(ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "name",
            "is_significant_activity",
            "is_negative_activity",
            "is_all_day_activity",
            "notes",
            "created",
            "modified",
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
