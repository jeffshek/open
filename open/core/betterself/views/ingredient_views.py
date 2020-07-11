import logging

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.serializers.ingredient_serializers import (
    IngredientReadSerializer,
    IngredientCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)

logger = logging.getLogger(__name__)


class IngredientCreateListView(BaseCreateListView):
    model_class = Ingredient
    read_serializer_class = IngredientReadSerializer
    create_serializer_class = IngredientCreateUpdateSerializer


class IngredientGetUpdateView(BaseGetUpdateDeleteView):
    model_class = Ingredient
    read_serializer_class = IngredientReadSerializer
    update_serializer_class = IngredientCreateUpdateSerializer
