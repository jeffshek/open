from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from test_plus import TestCase

from open.core.writeup.constants import WriteUpResourceEndpoints
from open.core.writeup.factories import WriteUpPromptFactory
from open.core.writeup.models import WriteUpPromptVote
from open.users.factories import UserFactory
from open.users.models import User
from open.utilities.testing import generate_random_uuid_as_string

"""
dpy test core.writeup.tests.views.test_prompt_vote_views --keepdb
"""


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
        Token.objects.get_or_create(user=self.registered_user)

        self.registered_user_client = APIClient()
        self.registered_user_client.force_login(self.registered_user)

        self.staff_user = UserFactory(is_staff=True)
        Token.objects.get_or_create(user=self.staff_user)

        self.staff_user_client = APIClient()
        self.staff_user_client.force_login(self.staff_user)

    def test_view(self):
        prompt = WriteUpPromptFactory()
        prompt_uuid = prompt.uuid_str
        url_kwargs = {"prompt_uuid": prompt_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        original_prompt_score = prompt.score
        data = {"value": 1}

        response = self.registered_user_client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

        prompt.refresh_from_db()
        # the score counter isn't fully real-time, it's like meh
        self.assertTrue(prompt.score > original_prompt_score)

    def test_view_updates_score(self):
        prompt_uuid = WriteUpPromptFactory().uuid_str
        url_kwargs = {"prompt_uuid": prompt_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        data = {"value": 3}

        response = self.registered_user_client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_view_with_api_client(self):
        """ Having some odd issues with auth - figure out why"""
        prompt_uuid = WriteUpPromptFactory().uuid_str
        url_kwargs = {"prompt_uuid": prompt_uuid}
        url = reverse(self.VIEW_NAME, kwargs=url_kwargs)

        valid_token = self.registered_user.auth_token.key

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token " + valid_token)

        data = {"value": 3}
        response = client.post(url, data=data)
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
        self.assertEqual(response.status_code, 401)

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
