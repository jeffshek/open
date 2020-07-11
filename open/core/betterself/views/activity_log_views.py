from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.serializers.activity_log_serializers import (
    ActivityLogReadSerializer,
    ActivityLogCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)


class ActivityLogCreateListView(BaseCreateListView):
    model_class = ActivityLog
    read_serializer_class = ActivityLogReadSerializer
    create_serializer_class = ActivityLogCreateUpdateSerializer


class ActivityLogGetUpdateView(BaseGetUpdateDeleteView):
    model_class = ActivityLog
    read_serializer_class = ActivityLogReadSerializer
    update_serializer_class = ActivityLogCreateUpdateSerializer
