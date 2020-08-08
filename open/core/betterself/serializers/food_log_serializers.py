from rest_framework.exceptions import ValidationError
from rest_framework.fields import UUIDField

from open.core.betterself.models.food import Food
from open.core.betterself.models.food_logs import FoodLog
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.simple_generic_serializer import (
    create_name_uuid_serializer,
)
from open.core.betterself.serializers.validators import ModelValidatorsMixin


class FoodLogReadSerializer(BaseModelReadSerializer):
    food = create_name_uuid_serializer(Food)

    class Meta:
        model = FoodLog
        fields = (
            "uuid",
            "food",
            "time",
            "notes",
            "created",
            "modified",
            "display_name",
            "quantity",
        )


class FoodLogCreateUpdateSerializer(BaseCreateUpdateSerializer, ModelValidatorsMixin):
    food_uuid = UUIDField(source="food.uuid")

    class Meta:
        model = FoodLog
        fields = (
            "food_uuid",
            "quantity",
            "time",
            "notes",
            "user",
        )

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if validated_data.get("food"):
            food_uuid = validated_data.pop("food")["uuid"]
            food = Food.objects.get(uuid=food_uuid, user=user)
            validated_data["food"] = food

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user, food=food, time=validated_data["time"],
            ).exists():
                raise ValidationError(f"Fields user, food, and time are not unique!")

        return validated_data
