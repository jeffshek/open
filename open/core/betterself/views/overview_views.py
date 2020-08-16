from rest_framework.response import Response
from rest_framework.views import APIView


class OverviewView(APIView):
    def get(self, request, period):
        return Response()
