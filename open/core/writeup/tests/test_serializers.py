from django.test import TestCase

from open.core.writeup.serializers import (
    GPT2MediumPromptSerializer,
    WriteUpPromptCreateReadSerializer,
)


class WriteupPromptSerializerTests(TestCase):
    def test_serializer_returns_invalid_on_empty_prompts(self):
        data = {"prompt": "", "temperature": 1}

        serializer = GPT2MediumPromptSerializer(data=data)
        valid = serializer.is_valid()

        self.assertFalse(valid)


class WriteUpPromptSerializerTests(TestCase):
    def test_serializer_works(self):
        text = "I am so hungry for Shake Shack right now"
        data = {"text": text, "email": text, "title": text}

        serializer = WriteUpPromptCreateReadSerializer(data=data)
        valid = serializer.is_valid()

        self.assertTrue(valid)
