import logging

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

"""
conceptually very similar to https://www.django-rest-framework.org/api-guide/generic-views/

just implemented in a way that i prefer fine-grained control over.

but even to this day ... i sort of wonder if I should have just made my logic fit generic views versus rolling my own here.
"""


class BaseCreateListView(APIView):
    model_class = None
    read_serializer_class = None
    create_serializer_class = None
    select_related_models = []
    prefetch_related_models = []
    filter_backends = []

    def get(self, request):
        # if passed in for select_related_models, use whatever is passed in
        # this will work, however, i removed it from most of the models since it wasn't necessary
        if self.select_related_models:
            instances = self.model_class.objects.filter(
                user=request.user
            ).select_related(*self.select_related_models)
        else:
            instances = self.model_class.objects.filter(
                user=request.user
            ).select_related()

        if self.prefetch_related_models:
            instances = instances.prefetch_related(*self.prefetch_related_models)

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

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset


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
