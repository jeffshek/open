from django.db.models import UUIDField
from rest_framework import serializers
from rest_framework.fields import IntegerField

from open.core.writeup.models import WriteUpPrompt, WriteUpFlaggedPrompt


class GPT2MediumPromptSerializer(serializers.Serializer):
    # warning!
    # copy and pasted from service repo, the only modifications to this should be one way
    # synced from other repo
    prompt = serializers.CharField(required=True)
    batch_size = serializers.IntegerField(default=5, max_value=10, min_value=1)
    length = serializers.IntegerField(default=40, max_value=1024, min_value=1)
    temperature = serializers.FloatField(default=.7, min_value=0.1, max_value=1)
    top_k = serializers.IntegerField(default=10, max_value=40)


class WriteUpPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriteUpPrompt
        fields = ("text", "email", "title", "uuid", "instagram", "twitter", "website")


class WriteUpPromptVoteModifySerializer(serializers.ModelSerializer):
    prompt_uuid = UUIDField(required=True)
    value = IntegerField(min_value=-1, max_value=3, default=1)

    class Meta:
        model = WriteUpPrompt
        fields = ("prompt_uuid", "value")


class WriteUpFlaggedPromptModifySerializer(serializers.ModelSerializer):
    prompt_uuid = UUIDField(required=True)

    class Meta:
        model = WriteUpFlaggedPrompt
