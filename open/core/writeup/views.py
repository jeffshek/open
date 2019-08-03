import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.writeup.models import WriteUpSharedPrompt
from open.core.writeup.serializers import WriteUpSharedPromptSerializer

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


def writeup_index(request):
    return render(request, "writeup/index.html", {})


def writeup_room(request, room_name):
    return render(
        request,
        "writeup/room.html",
        {"room_name_json": mark_safe(json.dumps(room_name))},
    )


class WriteUpSharedPromptView(APIView):
    permission_classes = ()

    def get(self, request, uuid):
        prompt = WriteUpSharedPrompt(uuid=uuid)
        serializer = WriteUpSharedPromptSerializer(prompt)
        data = serializer.data

        return Response(data=data)

    def post(self, request):
        serializer = WriteUpSharedPromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()

        instanced_serialized = WriteUpSharedPromptSerializer(instance)
        return Response(data=instanced_serialized.data)
