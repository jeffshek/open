import logging

from open.core.betterself.models.supplement import Supplement
from open.core.betterself.serializers.supplement_serializers import (
    SupplementReadSerializer,
    SupplementCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)

logger = logging.getLogger(__name__)


class SupplementCreateListView(BaseCreateListView):
    model_class = Supplement
    read_serializer_class = SupplementReadSerializer
    create_serializer_class = SupplementCreateUpdateSerializer


class SupplementGetUpdateView(BaseGetUpdateDeleteView):
    model_class = Supplement
    read_serializer_class = SupplementReadSerializer
    update_serializer_class = SupplementCreateUpdateSerializer
