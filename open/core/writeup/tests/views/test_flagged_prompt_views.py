from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from test_plus import TestCase

from open.core.writeup.constants import WriteUpResourceEndpoints
from open.core.writeup.factories import (
    WriteUpPromptFactory,
    WriteUpFlaggedPromptFactory,
)
from open.core.writeup.models import WriteUpFlaggedPrompt
from open.users.factories import UserFactory
from open.users.models import User
from open.utilities.testing import generate_random_uuid_as_string


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
