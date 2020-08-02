from open.core.betterself.models.food_logs import FoodLog
from open.core.betterself.serializers.food_log_serializers import (
    FoodLogReadSerializer,
    FoodLogCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)


class FoodLogCreateListView(BaseCreateListView):
    model_class = FoodLog
    read_serializer_class = FoodLogReadSerializer
    create_serializer_class = FoodLogCreateUpdateSerializer


class FoodLogGetUpdateView(BaseGetUpdateDeleteView):
    model_class = FoodLog
    read_serializer_class = FoodLogReadSerializer
    update_serializer_class = FoodLogCreateUpdateSerializer
