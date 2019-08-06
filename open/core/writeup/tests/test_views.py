from rest_framework.reverse import reverse

from open.core.writeup.constants import WriteUpResourceEndpoints
from open.core.writeup.factories import WriteUpPromptFactory
from open.core.writeup.models import WriteUpPrompt
from open.utilities.testing_mixins import OpenDefaultTest


class WriteupViewTests(OpenDefaultTest):
    """
    dpy test core.writeup
    """

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
