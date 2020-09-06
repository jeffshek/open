import logging

from rest_framework.response import Response

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

    def post(self, request):
        context = {"request": request}
        serializer = self.create_serializer_class(data=request.data, context=context)

        serializer.is_valid(raise_exception=True)

        # normal operation, proceed as normal
        if "supplement" in serializer.validated_data:
            instance = serializer.save()
            serialized_data = self.read_serializer_class(instance).data
        else:
            # supplement_stack - do some non-elegant stuff
            instances = serializer.save()
            serialized_data = self.read_serializer_class(instances, many=True).data

        return Response(serialized_data)


class SupplementLogGetUpdateView(BaseGetUpdateDeleteView):
    model_class = SupplementLog
    read_serializer_class = SupplementLogReadSerializer
    update_serializer_class = SupplementLogCreateUpdateSerializer
