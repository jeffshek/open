from rest_framework.exceptions import ValidationError

from open.core.betterself.models.food import Food
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)


class FoodReadSerializer(BaseModelReadSerializer):
    class Meta:
        model = Food
        fields = (
            "uuid",
            "name",
            "notes",
            "created",
            "modified",
            "display_name",
            "calories",
            "is_liquid",
        )


class FoodCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Food
        fields = ("name", "notes", "user", "calories", "is_liquid")

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user, name=validated_data["name"],
            ).exists():
                raise ValidationError(f"Fields user and name are not unique!")

        return validated_data
