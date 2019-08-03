from django.test import TestCase

from open.core.writeup.constants import GPT2_END_TEXT_STRING
from open.core.writeup.utilities import (
    serialize_gpt2_individual_values,
    serialize_gpt2_api_response,
)


class TestUtilities(TestCase):
    def test_gpt2_text_cleanup(self):
        fresh_prince = (
            "Now this is a story all about how\n\nMy life got flipped upside down"
        )
        two_of_us = "Just the two of us, building castles in the sky, Just the two of us, you and I"
        mock_response = fresh_prince + GPT2_END_TEXT_STRING + two_of_us

        serialized = serialize_gpt2_individual_values(mock_response)
        self.assertEqual(fresh_prince, serialized)

    def test_gpt2_text_cleanup_remove_new_lines(self):
        too_many_newlines = "\n\nCat\n\n"

        serialized = serialize_gpt2_individual_values(too_many_newlines)
        self.assertEqual("Cat", serialized)

    def test_gpt2_api_serializer(self):
        """ Make sure a method translates an API response into a django channels consumable one"""
        text_with_spaces = " I have lot of spaces         "
        data = {"prompt": "Spiderman", "text_0": text_with_spaces}

        serialized_data = serialize_gpt2_api_response(data)

        expected_data = data.copy()
        expected_data["text_0"] = text_with_spaces.strip()

        self.assertEqual(serialized_data, expected_data)
