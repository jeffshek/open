import logging

from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.core.betterself.serializers.supplement_stack_composition_serializers import (
    SupplementStackCompositionReadSerializer,
    SupplementStackCompositionCreateUpdateSerializer,
)
from open.core.betterself.views.mixins import (
    BaseGetUpdateDeleteView,
    BaseCreateListView,
)

logger = logging.getLogger(__name__)


class SupplementStackCompositionCreateListView(BaseCreateListView):
    model_class = SupplementStackComposition
    read_serializer_class = SupplementStackCompositionReadSerializer
    create_serializer_class = SupplementStackCompositionCreateUpdateSerializer


class SupplementStackCompositionGetUpdateView(BaseGetUpdateDeleteView):
    model_class = SupplementStackComposition
    read_serializer_class = SupplementStackCompositionReadSerializer
    update_serializer_class = SupplementStackCompositionCreateUpdateSerializer
