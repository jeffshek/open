from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from test_plus import TestCase

from open.core.writeup.constants import (
    WriteUpResourceEndpoints,
    PromptShareStates,
    StaffVerifiedShareStates,
)
from open.core.writeup.factories import (
    WriteUpPromptFactory,
    WriteUpFlaggedPromptFactory,
)
from open.core.writeup.models import (
    WriteUpPrompt,
    WriteUpPromptVote,
    WriteUpFlaggedPrompt,
)
from open.users.factories import UserFactory
from open.users.models import User
from open.utilities.testing import generate_random_uuid_as_string
from open.utilities.testing_mixins import OpenDefaultTest, OpenDefaultAPITest

"""
dpy test core.writeup.tests.test_views --keepdb
"""


class GPT2MediumPromptDebugViewTests(OpenDefaultTest):
    VIEW_NAME = WriteUpResourceEndpoints.GENERATED_SENTENCE
    VIEW_NEEDS_LOGIN = False

    def test_get_view(self):
        response = self._get_response_data()
        self.assertTrue("prompt" in response)


class WriteUpPromptViewTests(OpenDefaultAPITest):
    VIEW_NAME = WriteUpResourceEndpoints.PROMPTS

    def test_get_view(self):
        mock_title = "I Want Noodles"
        prompt = WriteUpPromptFactory(title=mock_title, user=self.registered_user)
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["uuid"], prompt.uuid_str)
        self.assertEqual(data["title"], prompt.title)

    def test_get_view_no_permission(self):
        mock_title = "I Want Noodles"
        prompt = WriteUpPromptFactory(title=mock_title)
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_view_marked_as_public_can_be_accessed(self):
        mock_title = "I Want Noodles"
        prompt = WriteUpPromptFactory(
            title=mock_title, share_state=PromptShareStates.PUBLISHED
        )
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["uuid"], prompt.uuid_str)
        self.assertEqual(data["title"], prompt.title)

    def test_get_view_marked_as_failed_flagged_cannot_be_accessed(self):
        mock_title = "I Want Noodles"
        prompt = WriteUpPromptFactory(
            title=mock_title,
            share_state=PromptShareStates.PUBLISHED,
            staff_verified_share_state=StaffVerifiedShareStates.VERIFIED_FAIL,
        )
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_view(self):
        url = reverse(self.VIEW_NAME)

        text = "I am eating a hamburger"
        data = {"text": text, "email": text, "title": text}

        client = self.registered_user_client
        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        returned_uuid = response.data["uuid"]
        returned_text = response.data["text"]

        self.assertEqual(returned_text, text)

        created_instance = WriteUpPrompt.objects.get(uuid=returned_uuid)
        self.assertEqual(created_instance.text, text)

        # since this was passed by a registered user, make sure user owns it
        self.assertEqual(created_instance.user, self.registered_user)

    def test_post_view_share_state(self):
        url = reverse(self.VIEW_NAME)

        text = "I am eating a hamburger"
        data = {
            "text": text,
            "email": text,
            "title": text,
            "share_state": PromptShareStates.PUBLISHED,
        }

        client = self.registered_user_client
        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        returned_uuid = response.data["uuid"]
        returned_text = response.data["text"]

        self.assertEqual(returned_text, text)

        created_instance = WriteUpPrompt.objects.get(uuid=returned_uuid)
        self.assertEqual(created_instance.share_state, PromptShareStates.PUBLISHED)

    def test_post_view_with_anon_user(self):
        url = reverse(self.VIEW_NAME)
        text = "I am eating a hamburger"
        data = {"text": text, "email": text, "title": text}

        client = self.unregistered_user_client
        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        returned_uuid = response.data["uuid"]
        returned_text = response.data["text"]

        self.assertEqual(returned_text, text)

        created_instance = WriteUpPrompt.objects.get(uuid=returned_uuid)
        self.assertEqual(created_instance.text, text)

        # no logged in user made this, no user should be attached
        self.assertIsNone(created_instance.user)

    def test_post_view_multiple_times_creates_new_records(self):
        url = reverse(self.VIEW_NAME)
        text = "I am eating a hamburger"
        data = {"text": text, "email": text, "title": text}

        client = self.registered_user_client

        for _ in range(5):
            response = client.post(url, data=data)
            self.assertEqual(response.status_code, 200)

        count = WriteUpPrompt.objects.filter(user=self.registered_user).count()
        self.assertEqual(count, 5)

    def test_delete_view(self):
        prompt = WriteUpPromptFactory(user=self.registered_user)
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        client = self.registered_user_client
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)

        exists = WriteUpPrompt.objects.filter(uuid=prompt.uuid_str).exists()
        self.assertFalse(exists)

    def test_list_view_wont_return_bad_stuff(self):
        WriteUpPromptFactory(
            staff_verified_share_state=StaffVerifiedShareStates.VERIFIED_FAIL
        )
        url = reverse(self.VIEW_NAME)

        response = self.registered_user_client.get(url)

        self.assertEqual(0, len(response.data))

    def test_list_view_returns_published_stuff(self):
        WriteUpPromptFactory.create_batch(5, share_state=PromptShareStates.PUBLISHED)
        WriteUpPromptFactory.create_batch(
            5, share_state=PromptShareStates.PUBLISHED_LINK_ACCESS_ONLY
        )
        WriteUpPromptFactory.create_batch(5, share_state=PromptShareStates.UNSHARED)

        url = reverse(self.VIEW_NAME)

        response = self.registered_user_client.get(url)

        # should only see 5, the ones that are PUBLISHED
        self.assertEqual(5, len(response.data))


class WriteUpPromptVoteViewTests(TestCase):
    VIEW_NAME = WriteUpResourceEndpoints.PROMPT_VOTES

    @classmethod
    def setUpTestData(cls):
        registered_user = UserFactory(is_staff=False)
        cls.registered_user_id = registered_user.id

        staff_user = UserFactory(is_staff=True)
        cls.staff_user_id = staff_user.id

    def setUp(self):
        self.unregistered_user_client = APIClient()

        self.registered_user = User.objects.get(id=self.registered_user_id)
        self.registered_user_client = APIClient()
        self.registered_user_client.force_login(self.registered_user)

        self.staff_user = UserFactory(is_staff=True)
        self.staff_user_client = APIClient()
        self.staff_user_client.force_login(self.staff_user)

    def test_view(self):
        prompt_uuid = WriteUpPromptFactory().uuid_str
        url_kwargs = {"prompt_uuid": prompt_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        data = {"value": 3}

        response = self.registered_user_client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_view_fake_uuid(self):
        fake_uuid = generate_random_uuid_as_string()
        url_kwargs = {"prompt_uuid": fake_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        data = {"value": 3}

        response = self.registered_user_client.post(url, data=data)
        self.assertEqual(response.status_code, 404)

    def test_no_login_has_no_access(self):
        prompt_uuid = WriteUpPromptFactory().uuid_str
        url_kwargs = {"prompt_uuid": prompt_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        data = {"value": 3}

        response = self.unregistered_user_client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_post_multiple_times_only_results_in_one_record(self):
        prompt_uuid = WriteUpPromptFactory().uuid_str
        url_kwargs = {"prompt_uuid": prompt_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        data = {"value": 3}

        for _ in range(3):
            self.registered_user_client.post(url, data=data)

        count = WriteUpPromptVote.objects.filter(
            user=self.registered_user, prompt__uuid=prompt_uuid
        ).count()
        self.assertEqual(count, 1)


class WriteUpFlaggedPromptViewTests(TestCase):
    VIEW_NAME = WriteUpResourceEndpoints.PROMPT_FLAGS

    @classmethod
    def setUpTestData(cls):
        registered_user = UserFactory(is_staff=False)
        cls.registered_user_id = registered_user.id

        staff_user = UserFactory(is_staff=True)
        cls.staff_user_id = staff_user.id

    def setUp(self):
        self.unregistered_user_client = APIClient()

        self.registered_user = User.objects.get(id=self.registered_user_id)
        self.registered_user_client = APIClient()
        self.registered_user_client.force_login(self.registered_user)

        self.staff_user = UserFactory(is_staff=True)
        self.staff_user_client = APIClient()
        self.staff_user_client.force_login(self.staff_user)

    def test_view(self):
        prompt = WriteUpPromptFactory()
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_post_view_multiple_times_only_results_in_one(self):
        prompt = WriteUpPromptFactory()
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        for _ in range(3):
            self.registered_user_client.post(url)

        instance_count = WriteUpFlaggedPrompt.objects.filter(
            user=self.registered_user, prompt=prompt
        ).count()
        self.assertEqual(instance_count, 1)

    def test_view_delete(self):
        prompt = WriteUpPromptFactory()
        WriteUpFlaggedPromptFactory(user=self.registered_user, prompt=prompt)

        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_view_delete_doesnt_exist(self):
        data_kwargs = {"prompt_uuid": generate_random_uuid_as_string()}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.delete(url)
        self.assertEqual(response.status_code, 404)
