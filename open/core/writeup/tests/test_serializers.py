from django.test import TestCase

from open.core.writeup.serializers import GPT2MediumPromptSerializer


class WriteupSerializerTests(TestCase):
    def test_serializer_returns_invalid_on_empty_prompts(self):
        data = {"prompt": "", "temperature": 1}

        serializer = GPT2MediumPromptSerializer(data=data)
        valid = serializer.is_valid()

        self.assertFalse(valid)
