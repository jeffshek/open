from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.writeup.models import WriteUpPrompt
from open.core.writeup.serializers import WriteUpPromptSerializer

SENTENCE_1_MOCK_RESPONSE = "API Services: ONLINE."


class GPT2MediumPromptTestView(APIView):
    """ A Quick Test View To Use When Debugging """

    permission_classes = ()

    def get(self, request):
        response = {
            "prompt": "Hello, I am a useful test to see baseline performance",
            "text_0": "Tell Me How Long",
            "text_1": "It takes to run a query, so that I can be used to benchmark",
            "text_2": "Other performances ... ",
        }

        return Response(data=response)

    def post(self, request):
        response = {
            "prompt": "Hello, I am a useful test to see baseline performance",
            "text_0": "Tell Me How Long",
            "text_1": "It takes to run a query, so that I can be used to benchmark",
            "text_2": "Other performances ... ",
        }

        return Response(data=response)


class WriteUpPromptView(APIView):
    permission_classes = ()

    def get(self, request, uuid):
        prompt = WriteUpPrompt(uuid=uuid)
        serializer = WriteUpPromptSerializer(prompt)
        data = serializer.data

        return Response(data=data)

    def post(self, request):
        serializer = WriteUpPromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        instanced_serialized = WriteUpPromptSerializer(instance)
        return Response(data=instanced_serialized.data)
