from django.test import TestCase

from open.core.writeup.caches import get_cache_key_for_gpt2_parameter
from open.core.writeup.constants import MLModelNames
from open.core.writeup.serializers import TextAlgorithmPromptSerializer


class TestWriteUpCaches(TestCase):
    def test_cache_key(self):
        prompt = "Testing A Cache Key\n"
        batch_size = 5
        length = 10
        temperature = 0.7
        top_k = 40

        cache_key = get_cache_key_for_gpt2_parameter(
            prompt, batch_size, length, temperature, top_k
        )
        expected_result = f"writeup_6a8d5bebad2295c438c3c26c28813f80_5_10_0.7_40_" f"english_common_{MLModelNames.GPT2_MEDIUM}"

        self.assertEqual(cache_key, expected_result)

    def test_cache_key_with_new_line(self):
        prompt = "Testing A Cache Key\n"
        batch_size = 5
        length = 10
        temperature = 0.7
        top_k = 40

        cache_key = get_cache_key_for_gpt2_parameter(
            prompt, batch_size, length, temperature, top_k
        )
        expected_result = f"writeup_6a8d5bebad2295c438c3c26c28813f80_5_10_0.7_40_" f"english_common_{MLModelNames.GPT2_MEDIUM}"

        self.assertEqual(cache_key, expected_result)

    def test_cache_key_with_space(self):
        prompt = "Testing A Cache Key\n   "
        batch_size = 5
        length = 10
        temperature = 0.7
        top_k = 40

        cache_key = get_cache_key_for_gpt2_parameter(
            prompt, batch_size, length, temperature, top_k
        )
        expected_result = f"writeup_6a8d5bebad2295c438c3c26c28813f80_5_10_0.7_40_" f"english_common_{MLModelNames.GPT2_MEDIUM}"

        self.assertEqual(cache_key, expected_result)

    def test_cache_key_with_serializer(self):
        post_message = {"prompt": "Hello"}

        serializer = TextAlgorithmPromptSerializer(data=post_message)
        serializer.is_valid(raise_exception=False)

        cache_key = get_cache_key_for_gpt2_parameter(**serializer.validated_data)

        expected_cache_key = f"writeup_8b1a9953c4611296a827abf8c47804d7_5_40_0.7_10_" f"english_common_{MLModelNames.GPT2_MEDIUM}"
        self.assertEqual(cache_key, expected_cache_key)
