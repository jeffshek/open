from rest_framework.serializers import ModelSerializer

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.serializers.mixins import BaseCreateUpdateSerializer
from open.users.serializers import SimpleUserReadSerializer


class IngredientReadSerializer(ModelSerializer):
    user = SimpleUserReadSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = [
            "half_life_minutes",
            "name",
            "notes",
            "user",
            "uuid",
            "created",
            "modified",
        ]


class IngredientCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Ingredient
        fields = ["half_life_minutes", "name", "notes", "user", "uuid"]
