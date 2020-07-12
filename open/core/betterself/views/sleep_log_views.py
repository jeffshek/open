from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.serializers.sleep_log_serializers import (
    SleepLogReadSerializer,
    SleepLogCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)


class SleepLogCreateListView(BaseCreateListView):
    model_class = SleepLog
    read_serializer_class = SleepLogReadSerializer
    create_serializer_class = SleepLogCreateUpdateSerializer


class SleepLogGetUpdateView(BaseGetUpdateDeleteView):
    model_class = SleepLog
    read_serializer_class = SleepLogReadSerializer
    update_serializer_class = SleepLogCreateUpdateSerializer
