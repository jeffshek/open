import logging

from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.serializers.supplement_log_serializers import (
    SupplementLogReadSerializer,
    SupplementLogCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseCreateListView,
    BaseGetUpdateDeleteView,
)

logger = logging.getLogger(__name__)


class SupplementLogCreateListView(BaseCreateListView):
    model_class = SupplementLog
    read_serializer_class = SupplementLogReadSerializer
    create_serializer_class = SupplementLogCreateUpdateSerializer


class SupplementLogGetUpdateView(BaseGetUpdateDeleteView):
    model_class = SupplementLog
    read_serializer_class = SupplementLogReadSerializer
    update_serializer_class = SupplementLogCreateUpdateSerializer
