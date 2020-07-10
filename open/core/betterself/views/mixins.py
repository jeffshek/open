from rest_framework.response import Response
from rest_framework.views import APIView


class BaseCreateListView(APIView):
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
