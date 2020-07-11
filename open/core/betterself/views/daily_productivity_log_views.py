from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.serializers.daily_productivity_log_serializers import (
    DailyProductivityLogReadSerializer,
    DailyProductivityLogCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)


class DailyProductivityLogCreateListView(BaseCreateListView):
    model_class = DailyProductivityLog
    read_serializer_class = DailyProductivityLogReadSerializer
    create_serializer_class = DailyProductivityLogCreateUpdateSerializer


class DailyProductivityLogGetUpdateView(BaseGetUpdateDeleteView):
    model_class = DailyProductivityLog
    read_serializer_class = DailyProductivityLogReadSerializer
    update_serializer_class = DailyProductivityLogCreateUpdateSerializer
