import logging

from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.serializers.supplement_stack_serializers import (
    SupplementStackReadSerializer,
    SupplementStackCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)

logger = logging.getLogger(__name__)


class SupplementStackCreateListView(BaseCreateListView):
    model_class = SupplementStack
    read_serializer_class = SupplementStackReadSerializer
    create_serializer_class = SupplementStackCreateUpdateSerializer


class SupplementStackGetUpdateView(BaseGetUpdateDeleteView):
    model_class = SupplementStack
    read_serializer_class = SupplementStackReadSerializer
    update_serializer_class = SupplementStackCreateUpdateSerializer
