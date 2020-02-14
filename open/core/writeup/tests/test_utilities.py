from django.conf import settings
from django.test import TestCase

from open.core.writeup.constants import (
    GPT2_END_TEXT_STRING,
    StaffVerifiedShareStates,
    PromptShareStates,
    MLModelNames,
    TransformerXLNetTokenTypes,
)
from open.core.writeup.consumers import get_api_endpoint_from_model_name
from open.core.writeup.factories import WriteUpPromptFactory
from open.core.writeup.utilities.access_permissions import user_can_read_prompt_instance
from open.core.writeup.utilities.text_algo_serializers import (
    serialize_text_algo_individual_values,
    serialize_text_algo_api_response_sync,
)
from open.users.factories import UserFactory

"""
dpy test core.writeup.tests.test_utilities --keepdb
"""


class TestGPT2SerializerUtilities(TestCase):
    def test_gpt2_text_cleanup(self):
        fresh_prince = (
            "Now this is a story all about how\n\nMy life got flipped upside down"
        )
        two_of_us = "Just the two of us, building castles in the sky, Just the two of us, you and I"
        mock_response = fresh_prince + GPT2_END_TEXT_STRING + two_of_us

        serialized = serialize_text_algo_individual_values(mock_response)
        self.assertEqual(fresh_prince, serialized)

    def test_gpt2_text_cleanup_multiple_end_of_text(self):
        fresh_prince = (
            "Now this is a story all about how\n\nMy life got flipped upside down"
        )
        two_of_us = "Just the two of us, building castles in the sky, Just the two of us, you and I"
        mock_response = fresh_prince + GPT2_END_TEXT_STRING + two_of_us

        mock_response = mock_response + GPT2_END_TEXT_STRING + "RANDOM"

        serialized = serialize_text_algo_individual_values(mock_response)
        self.assertEqual(fresh_prince, serialized)

    def test_gpt2_text_cleanup_remove_new_lines(self):
        too_many_newlines = "\n\nCat\n\n"

        serialized = serialize_text_algo_individual_values(too_many_newlines)
        self.assertEqual("Cat", serialized)

    def test_gpt2_api_serializer(self):
        """ Make sure a method translates an API response into a django channels consumable one"""
        text_with_spaces = " I have lot of spaces         "
        data = {"prompt": "Spiderman", "text_0": text_with_spaces}

        serialized_data = serialize_text_algo_api_response_sync(data)

        expected_data = data.copy()
        expected_data["text_0"] = text_with_spaces.strip()

        self.assertEqual(serialized_data, expected_data)


class TestTransformerSerializerUtilities(TestCase):
    def test_beginning_of_prompts_removes_after(self):
        start = "the beginning of the prompt"
        text_with_beginning_promt = f"{start}{TransformerXLNetTokenTypes.BEGINNING_OF_PROMPT} nothing should show up"

        result = serialize_text_algo_individual_values(text_with_beginning_promt)
        self.assertEqual(result, start)

    def test_end_of_prompts_removes_after(self):
        start = "the beginning of the prompt"
        text_with_beginning_promt = f"{start}{TransformerXLNetTokenTypes.ENDING_OF_PROMPT} nothing should show up"

        result = serialize_text_algo_individual_values(text_with_beginning_promt)
        self.assertEqual(result, start)

    def test_end_of_paragraph_returns_double_space(self):
        text = "the beginning of the prompt"
        text_with_token = f"{text}{TransformerXLNetTokenTypes.ENDING_OF_PARAGRAPH}should have multiple newlines {TransformerXLNetTokenTypes.ENDING_OF_PARAGRAPH}"

        result = serialize_text_algo_individual_values(text_with_token)
        new_line_count = result.count("\n")
        # two end of paragraphs should return 4 new lines
        self.assertEqual(new_line_count, 4)

    def test_unknown_tokens_dont_show_up(self):
        text = "the beginning of the prompt"
        text_with_token = f"{text}{TransformerXLNetTokenTypes.UNKNOWN_TOKEN} tell me a story {TransformerXLNetTokenTypes.UNKNOWN_TOKEN}"
        result = serialize_text_algo_individual_values(text_with_token)
        unknown_count = result.count(TransformerXLNetTokenTypes.UNKNOWN_TOKEN)

        self.assertEqual(unknown_count, 0)


class TestAccessPermissionsForPrompts(TestCase):
    def test_access_permission_for_user_owner(self):
        user = UserFactory()
        user_prompt = WriteUpPromptFactory(user=user)
        valid = user_can_read_prompt_instance(user, user_prompt)

        self.assertTrue(valid)

    def test_access_permission_for_not_owner(self):
        user = UserFactory()

        diff_user_prompt = WriteUpPromptFactory()
        valid = user_can_read_prompt_instance(user, diff_user_prompt)

        self.assertFalse(valid)

    def test_access_permission_for_not_owner_failed(self):
        user = UserFactory()

        diff_user_prompt = WriteUpPromptFactory(
            share_state=PromptShareStates.PUBLISHED,
            staff_verified_share_state=StaffVerifiedShareStates.VERIFIED_FAIL,
        )
        valid = user_can_read_prompt_instance(user, diff_user_prompt)

        self.assertFalse(valid)


class TestAPIEndpointsUrlCorrect(TestCase):
    def test_api_endpoints_correctly_returned(self):
        returned_endpoint = get_api_endpoint_from_model_name(MLModelNames.GPT2_LARGE)
        self.assertEqual(returned_endpoint, settings.GPT2_LARGE_API_ENDPOINT)

    def test_api_endpoints_correctly_returned_two(self):
        returned_endpoint = get_api_endpoint_from_model_name(
            MLModelNames.XLNET_BASE_CASED
        )
        self.assertEqual(returned_endpoint, settings.XLNET_BASE_CASED_API_ENDPOINT)
