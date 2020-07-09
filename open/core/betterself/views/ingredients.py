import logging

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.serializers import (
    IngredientReadSerializer,
    IngredientCreateSerializer,
    IngredientUpdateSerializer,
)

logger = logging.getLogger(__name__)


class IngredientCreateListView(APIView):
    model_class = Ingredient
    read_serializer_class = IngredientReadSerializer
    create_serializer_class = IngredientCreateSerializer

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


class IngredientGetUpdateView(APIView):
    model_class = Ingredient
    read_serializer_class = IngredientReadSerializer
    update_serializer_class = IngredientUpdateSerializer

    def get(self, request, uuid):
        instance = get_object_or_404(self.model_class, user=request.user, uuid=uuid)
        data = self.read_serializer_class(instance).data
        return Response(data)

    def post(self, request, uuid):
        instance = get_object_or_404(self.model_class, user=request.user, uuid=uuid)

        context = {"request": request}
        serializer = self.update_serializer_class(
            instance, data=request.data, context=context, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serialized_instance = self.read_serializer_class(instance).data
        return Response(serialized_instance)

    def delete(self, request, uuid):
        instance = get_object_or_404(self.model_class, user=request.user, uuid=uuid)
        instance.delete()

        label = (
            f"DELETED | {self.model_class} | ID {instance.id} deleted by {request.user}"
        )
        logger.info(label)

        return Response(status=204)
