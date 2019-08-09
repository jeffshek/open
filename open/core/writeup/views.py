from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from open.core.writeup.constants import (
    SHOWABLE_STAFF_VERIFIED_STATES,
    PromptShareStates,
)
from open.core.writeup.models import (
    WriteUpPrompt,
    WriteUpPromptVote,
    WriteUpFlaggedPrompt,
)
from open.core.writeup.serializers import (
    WriteUpPromptCreateReadSerializer,
    WriteUpPromptVoteModifySerializer,
)
from open.core.writeup.utilities.access_permissions import user_can_read_prompt_instance

SENTENCE_1_MOCK_RESPONSE = "API Services: ONLINE."


class GPT2MediumPromptDebugView(APIView):
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


class WriteUpPromptListCreateView(APIView):
    permission_classes = ()
    throttle_scope = "default_scope"

    def get_throttles(self):
        if self.request.method.lower() == "get":
            self.throttle_scope = "list_prompt_rate"
        elif self.request.method.lower() == "post":
            self.throttle_scope = "create_prompt_rate"

        return super(WriteUpPromptListCreateView, self).get_throttles()

    def get(self, request):
        writeup_prompts = WriteUpPrompt.objects.filter(
            share_state=PromptShareStates.PUBLISHED,
            staff_verified_share_state__in=SHOWABLE_STAFF_VERIFIED_STATES,
        )

        serializer = WriteUpPromptCreateReadSerializer(writeup_prompts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WriteUpPromptCreateReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user.is_anonymous:
            user = None
        else:
            user = request.user

        instance = serializer.save(user=user)

        instanced_serialized = WriteUpPromptCreateReadSerializer(instance)
        return Response(data=instanced_serialized.data)


class WriteUpPromptView(APIView):
    permission_classes = ()

    def get(self, request, prompt_uuid):
        prompt = get_object_or_404(WriteUpPrompt, uuid=prompt_uuid)

        can_read = user_can_read_prompt_instance(request.user, prompt)
        if not can_read:
            raise Http404

        serializer = WriteUpPromptCreateReadSerializer(prompt)
        data = serializer.data

        return Response(data=data)

    def delete(self, request, prompt_uuid):
        if request.user.is_anonymous:
            raise Http404

        prompt = get_object_or_404(WriteUpPrompt, uuid=prompt_uuid, user=request.user)
        prompt.delete()

        return Response(status=204)


class WriteUpPromptVoteView(APIView):
    def post(self, request, prompt_uuid):
        prompt = get_object_or_404(WriteUpPrompt, uuid=prompt_uuid)
        user = request.user

        serializer = WriteUpPromptVoteModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        instance = WriteUpPromptVote.objects.update_or_create(
            user=user, prompt=prompt, defaults=validated_data
        )

        return_serializer = WriteUpPromptVoteModifySerializer(instance=instance)
        return Response(data=return_serializer.data)


class WriteUpFlaggedPromptView(APIView):
    def post(self, request, prompt_uuid):
        prompt = get_object_or_404(WriteUpPrompt, uuid=prompt_uuid)
        user = request.user

        WriteUpFlaggedPrompt.objects.update_or_create(prompt=prompt, user=user)

        # don't really need a serializer for this.
        data = {"status": f"{prompt_uuid} has been flagged. Thank you."}

        return Response(data=data)

    def delete(self, request, prompt_uuid):
        prompt = get_object_or_404(WriteUpPrompt, uuid=prompt_uuid)
        user = request.user

        instance = get_object_or_404(WriteUpFlaggedPrompt, prompt=prompt, user=user)
        instance.delete()

        return Response(status=204)
