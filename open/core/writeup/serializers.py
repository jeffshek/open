from rest_framework import serializers

from open.core.writeup.models import WriteUpPrompt


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
        fields = ("text", "email", "title", "uuid")
