from django.test import TestCase

from open.core.writeup.caches import get_cache_key_for_gpt2_parameter


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
        expected_result = (
            "writeup_6a8d5bebad2295c438c3c26c28813f80_5_10_0.7_40_english_common"
        )

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
        expected_result = (
            "writeup_6a8d5bebad2295c438c3c26c28813f80_5_10_0.7_40_english_common"
        )

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
        expected_result = (
            "writeup_6a8d5bebad2295c438c3c26c28813f80_5_10_0.7_40_english_common"
        )

        self.assertEqual(cache_key, expected_result)
