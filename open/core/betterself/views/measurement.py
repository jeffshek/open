from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.models.measurement import Measurement
from open.core.betterself.serializers.measurement_serializers import (
    MeasurementReadSerializer,
)


class MeasurementListView(APIView):
    model_class = Measurement
    read_serializer_class = MeasurementReadSerializer
    create_serializer_class = None
    update_serializer_class = None

    def get(self, request):
        # slightly different from other views because this doesn't filter on user
        instances = self.model_class.objects.all()
        serializer = self.read_serializer_class(instances, many=True)
        data = serializer.data
        return Response(data=data)
