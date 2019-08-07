from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from test_plus import TestCase

from open.core.writeup.constants import WriteUpResourceEndpoints
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
from open.utilities.testing_mixins import OpenDefaultTest

"""
dpy test core.writeup.tests.test_views --keepdb
"""


class WriteupViewTests(OpenDefaultTest):
    VIEW_NAME = WriteUpResourceEndpoints.GENERATED_SENTENCE
    VIEW_NEEDS_LOGIN = False

    def test_get_view(self):
        response = self._get_response_data()
        self.assertTrue("prompt" in response)


class WriteUpPromptViewTests(OpenDefaultTest):
    VIEW_NAME = WriteUpResourceEndpoints.PROMPTS
    VIEW_NEEDS_LOGIN = False

    @classmethod
    def setUpTestData(cls):
        cls.factory_uuid = WriteUpPromptFactory().uuid.__str__()
        super().setUpTestData()

    @classmethod
    def set_reversed_url(cls):
        kwargs = {"uuid": cls.factory_uuid}
        cls.url = reverse(cls.VIEW_NAME, kwargs=kwargs)

    def test_get_view(self):
        response = self._get_response()
        data = response.data
        self.assertEqual(data["uuid"], self.factory_uuid)

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

    def test_post_updating_already_existing_view_fails(self):
        url = reverse(self.VIEW_NAME)

        text = "I am eating a hamburger"
        data = {"text": text, "email": text, "title": text}

        client = self.registered_user_client
        response = client.post(url, data=data)
        returned_uuid = response.data["uuid"]

        # now try to pass a uuid in the post
        data["uuid"] = returned_uuid

        # this should ignore the uuid and make a new object instead
        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 200)
        new_uuid = response.data["uuid"]

        self.assertNotEqual(returned_uuid, new_uuid)


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
        prompt_uuid = WriteUpPromptFactory().uuid.__str__()
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
        prompt_uuid = WriteUpPromptFactory().uuid.__str__()
        url_kwargs = {"prompt_uuid": prompt_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        data = {"value": 3}

        response = self.unregistered_user_client.post(url, data=data)
        self.assertEqual(response.status_code, 403)

    def test_post_multiple_times_only_results_in_one_record(self):
        prompt_uuid = WriteUpPromptFactory().uuid.__str__()
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
        data_kwargs = {"prompt_uuid": prompt.uuid.__str__()}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_post_view_multiple_times_only_results_in_one(self):
        prompt = WriteUpPromptFactory()
        data_kwargs = {"prompt_uuid": prompt.uuid.__str__()}
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

        data_kwargs = {"prompt_uuid": prompt.uuid.__str__()}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_view_delete_doesnt_exist(self):
        data_kwargs = {"prompt_uuid": generate_random_uuid_as_string()}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        response = self.registered_user_client.delete(url)
        self.assertEqual(response.status_code, 404)
