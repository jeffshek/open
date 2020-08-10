import logging

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class BaseCreateListView(APIView):
    model_class = None
    read_serializer_class = None
    create_serializer_class = None
    select_related_models = []

    def get(self, request):
        # TODO - maybe change over a passed set of values, not sure, the default is working well ...
        # instances = self.model_class.objects.filter(user=request.user).select_related(*self.select_related_models)
        instances = self.model_class.objects.filter(user=request.user).select_related()

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


class BaseGetUpdateDeleteView(APIView):
    model_class = None
    read_serializer_class = None
    update_serializer_class = None

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
        label = (
            f"DELETED | {self.model_class} | ID {instance.id} deleted by {request.user}"
        )
        logger.info(label)
        instance.delete()

        return Response(status=204)
