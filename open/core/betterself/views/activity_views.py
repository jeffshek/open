from open.core.betterself.models.activity import Activity
from open.core.betterself.serializers.activity_serializers import (
    ActivityReadSerializer,
    ActivityCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)


class ActivityCreateListView(BaseCreateListView):
    model_class = Activity
    read_serializer_class = ActivityReadSerializer
    create_serializer_class = ActivityCreateUpdateSerializer


class ActivityGetUpdateView(BaseGetUpdateDeleteView):
    model_class = Activity
    read_serializer_class = ActivityReadSerializer
    update_serializer_class = ActivityCreateUpdateSerializer
