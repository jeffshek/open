from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.users.serializers import SimpleUserReadSerializer


class IngredientReadSerializer(BaseModelReadSerializer):
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
            "display_name",
        ]


class IngredientCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = Ingredient
        fields = ["half_life_minutes", "name", "notes", "user", "uuid"]
