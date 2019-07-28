import json

from django.utils.safestring import mark_safe
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render


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
