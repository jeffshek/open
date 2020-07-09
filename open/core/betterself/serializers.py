from rest_framework.fields import UUIDField, HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.models.supplement import Supplement
from open.users.serializers import SimpleUserReadSerializer


class SupplementReadSerializer(ModelSerializer):
    class Meta:
        model = Supplement
        fields = (
            "uuid",
            "notes",
            "name",
        )


class MeasurementReadSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "uuid",
            "name",
            "short_name",
            "is_liquid",
        )


class IngredientReadSerializer(ModelSerializer):
    user = SimpleUserReadSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes", "user")


class IngredientCreateSerializer(ModelSerializer):
    uuid = UUIDField(required=False, read_only=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes", "user")
        validators = [
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(), fields=["user", "name"]
            )
        ]

    def create(self, validated_data):
        create_model = self.Meta.model
        obj = create_model.objects.create(**validated_data)
        return obj


class IngredientUpdateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes", "user")
