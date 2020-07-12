from open.core.betterself.models.well_being_log import WellBeingLog
from open.core.betterself.serializers.well_being_log_serializers import (
    WellBeingLogReadSerializer,
    WellBeingLogCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)


class WellBeingLogCreateListView(BaseCreateListView):
    model_class = WellBeingLog
    read_serializer_class = WellBeingLogReadSerializer
    create_serializer_class = WellBeingLogCreateUpdateSerializer


class WellBeingLogGetUpdateView(BaseGetUpdateDeleteView):
    model_class = WellBeingLog
    read_serializer_class = WellBeingLogReadSerializer
    update_serializer_class = WellBeingLogCreateUpdateSerializer
