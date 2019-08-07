from django.test import TestCase

from open.core.writeup.constants import (
    GPT2_END_TEXT_STRING,
    StaffVerifiedShareStates,
    PromptShareStates,
)
from open.core.writeup.factories import WriteUpPromptFactory
from open.core.writeup.utilities.access_permissions import user_can_read_prompt_instance
from open.core.writeup.utilities.gpt2_serializers import (
    serialize_gpt2_individual_values,
    serialize_gpt2_api_response,
)
from open.users.factories import UserFactory

"""
dpy test core.writeup.tests.test_utilities --keepdb
"""


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
