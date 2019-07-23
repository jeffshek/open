from django.test import TestCase

from open.core.writeup.constants import GPT2_END_TEXT_STRING
from open.core.writeup.utilities import serialize_gpt2_responses


class TestUtilities(TestCase):
    def test_gpt2_text_cleanup(self):
        fresh_prince = (
            "Now this is a story all about how\n\nMy life got flipped upside down"
        )
        two_of_us = (
            "Just the two of us, building castles in the sky, Just the two of us, you and I"
        )
        mock_response = fresh_prince + GPT2_END_TEXT_STRING + two_of_us

        serialized = serialize_gpt2_responses(mock_response)
        self.assertEqual(fresh_prince, serialized)
