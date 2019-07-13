import json

from django.utils.safestring import mark_safe
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render


SENTENCE_1_MOCK_RESPONSE = "i hate cheese"


class GeneratedSentenceView(APIView):
    permission_classes = ()

    def get(self, request):
        data = {"sentence1": SENTENCE_1_MOCK_RESPONSE}
        return Response(data=data)


def writeup_index(request):
    return render(request, "writeup/index.html", {})


def writeup_room(request, room_name):
    return render(
        request,
        "writeup/room.html",
        {"room_name_json": mark_safe(json.dumps(room_name))},
    )
