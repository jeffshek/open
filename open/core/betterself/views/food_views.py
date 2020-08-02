from open.core.betterself.models.food import Food
from open.core.betterself.serializers.food_serializers import (
    FoodReadSerializer,
    FoodCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)


class FoodCreateListView(BaseCreateListView):
    model_class = Food
    read_serializer_class = FoodReadSerializer
    create_serializer_class = FoodCreateUpdateSerializer


class FoodGetUpdateView(BaseGetUpdateDeleteView):
    model_class = Food
    read_serializer_class = FoodReadSerializer
    update_serializer_class = FoodCreateUpdateSerializer
