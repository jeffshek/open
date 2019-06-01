from rest_framework.response import Response
from rest_framework.views import APIView


SENTENCE_1_MOCK_RESPONSE = "i hate cheese"

class GeneratedSentenceView(APIView):
    permission_classes = ()

    def get(self, request):
        data = {'sentence1': SENTENCE_1_MOCK_RESPONSE}
        return Response(data=data)
