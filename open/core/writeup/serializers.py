from rest_framework import serializers
from rest_framework.fields import IntegerField, UUIDField

from open.core.writeup.constants import ML_MODEL_NAME_CHOICES, MLModelNames
from open.core.writeup.models import (
    WriteUpPrompt,
    WriteUpFlaggedPrompt,
    WriteUpPromptVote,
)


class TextAlgorithmPromptSerializer(serializers.Serializer):
    # warning!
    # copy and pasted from service repo, the only modifications to this should be one way
    # synced from other repo
    prompt = serializers.CharField(required=True)
    batch_size = serializers.IntegerField(default=5, max_value=10, min_value=1)
    # cap off at 256 for now ... the frontend doesn't let someone put more than 50,
    # but it wouldn't be rocket science to reverse this endpoint considering the repo is oss lol
    length = serializers.IntegerField(default=40, max_value=256, min_value=1)
    temperature = serializers.FloatField(default=.7, min_value=0.1, max_value=1)
    top_k = serializers.IntegerField(default=10, max_value=40)
    top_p = serializers.FloatField(default=.7, max_value=1, min_value=0)
    model_name = serializers.ChoiceField(
        choices=ML_MODEL_NAME_CHOICES, default=MLModelNames.GPT2_MEDIUM
    )


class WriteUpPromptCreateReadSerializer(serializers.ModelSerializer):
    """
    PROMPTS
    """

    score = IntegerField(read_only=True)

    class Meta:
        model = WriteUpPrompt
        fields = (
            "text",
            "content",
            "email",
            "title",
            "uuid",
            "instagram",
            "twitter",
            "website",
            "share_state",
            "score",
            "created",
        )


class WriteUpPromptVoteModifySerializer(serializers.ModelSerializer):
    """
    VOTES
    """

    value = IntegerField(min_value=-1, max_value=3, default=1)

    class Meta:
        model = WriteUpPromptVote
        fields = ("value",)


class WriteUpFlaggedPromptModifySerializer(serializers.ModelSerializer):
    """
    FLAGGING
    """

    prompt_uuid = UUIDField(required=True)

    class Meta:
        model = WriteUpFlaggedPrompt
        fields = ("prompt_uuid",)
