from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.serializers import (
    MeasurementReadSerializer,
    IngredientReadSerializer,
    IngredientCreateSerializer,
)


class MeasurementListView(APIView):
    model_class = Measurement
    read_serializer_class = MeasurementReadSerializer
    create_serializer_class = None
    update_serializer_class = None

    def get(self, request):
        instances = self.model_class.objects.all()
        serializer = self.read_serializer_class(instances, many=True)
        data = serializer.data
        return Response(data=data)


class IngredientCreateListView(APIView):
    model_class = Ingredient
    read_serializer_class = IngredientReadSerializer
    create_serializer_class = IngredientCreateSerializer
    update_serializer_class = None

    def get(self, request):
        instances = self.model_class.objects.filter(user=request.user)
        serializer = self.read_serializer_class(instances, many=True)
        data = serializer.data
        return Response(data=data)

    def post(self, request):
        context = {"request": request}
        serializer = self.create_serializer_class(data=request.data, context=context)

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serialized_instance = self.read_serializer_class(instance).data
        return Response(serialized_instance)
