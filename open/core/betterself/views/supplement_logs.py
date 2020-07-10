import logging

from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.serializers.supplement_logs import (
    SupplementLogReadSerializer,
    SupplementLogCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import BaseCreateListView

logger = logging.getLogger(__name__)


class SupplementLogCreateListView(BaseCreateListView):
    model_class = SupplementLog
    read_serializer_class = SupplementLogReadSerializer
    create_serializer_class = SupplementLogCreateUpdateSerializer
