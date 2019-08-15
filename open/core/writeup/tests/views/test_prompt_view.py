from unittest import mock

from rest_framework.reverse import reverse

from open.core.writeup.constants import (
    WriteUpResourceEndpoints,
    PromptShareStates,
    StaffVerifiedShareStates,
)
from open.core.writeup.factories import WriteUpPromptFactory
from open.core.writeup.models import WriteUpPrompt
from open.utilities.testing_mixins import OpenDefaultAPITest


# dpy test core.writeup.tests.views.test_prompt_view --keepdb
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

    @mock.patch(
        "rest_framework.throttling.ScopedRateThrottle.get_rate", return_value="1/hour"
    )
    def test_post_view_hits_rate_limit_will_return_429(self, throttled_function):
        """
        because DRF imports settings in a non-standard manner, you can't use override settings
        to change the rate limit. by patching, you can get the same result.
        """
        url = reverse(self.VIEW_NAME)

        text = "I am eating a hamburger"
        data = {"text": text, "email": text, "title": text}

        client = self.registered_user_client

        for _ in range(3):
            response = client.post(url, data=data)

        # by the 3rd request, it should have hit the rate limit
        self.assertEqual(response.status_code, 429)

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

    def test_delete_view_wont_allow_for_not_owner(self):
        # prompt = WriteUpPromptFactory(user=self.registered_user)
        prompt = WriteUpPromptFactory()
        data_kwargs = {"prompt_uuid": prompt.uuid_str}
        url = reverse(self.VIEW_NAME, kwargs=data_kwargs)

        client = self.registered_user_client
        response = client.delete(url)
        self.assertEqual(response.status_code, 404)

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
        data = response.data

        # should only see 5, the ones that are PUBLISHED
        self.assertEqual(5, len(response.data))

        # we synthetically generate score on prompts
        result = data[0]
        self.assertIsNotNone(result["score"])

    def test_list_view_query_count(self):
        WriteUpPromptFactory.create_batch(100, share_state=PromptShareStates.PUBLISHED)
        WriteUpPromptFactory.create_batch(
            5, share_state=PromptShareStates.PUBLISHED_LINK_ACCESS_ONLY
        )
        WriteUpPromptFactory.create_batch(5, share_state=PromptShareStates.UNSHARED)
        url = reverse(self.VIEW_NAME)

        # it's currently five queries for the view / auth login / some permission checking
        with self.assertNumQueriesLessThan(6):
            response = self.registered_user_client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_list_view_returns_sorted_correctly(self):
        # should return greatest to smallest, that way easier to truncate
        WriteUpPromptFactory.create_batch(100, share_state=PromptShareStates.PUBLISHED)
        url = reverse(self.VIEW_NAME)
        response = self.registered_user_client.get(url)
        data = response.data

        score = [item["score"] for item in data]

        sorted_score = sorted(score, reverse=True)
        self.assertEqual(score, sorted_score)
