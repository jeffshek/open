import logging

from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.serializers.ingredient_composition_serializers import (
    IngredientCompositionReadSerializer,
    IngredientCompositionCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)

logger = logging.getLogger(__name__)


class IngredientCompositionCreateListView(BaseCreateListView):
    model_class = IngredientComposition
    read_serializer_class = IngredientCompositionReadSerializer
    create_serializer_class = IngredientCompositionCreateUpdateSerializer


class IngredientCompositionGetUpdateView(BaseGetUpdateDeleteView):
    model_class = IngredientComposition
    read_serializer_class = IngredientCompositionReadSerializer
    update_serializer_class = IngredientCompositionCreateUpdateSerializer
