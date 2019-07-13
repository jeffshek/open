from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from test_plus import APITestCase

from open.core.writeup.constants import WriteUpResourceEndpoints
from open.users.factories import UserFactory
from open.users.models import User


class OpenDefaultTest(APITestCase):
    """
    Note: This will also run itself once too ...
    This is a bit of an antipattern, I should separate as a mixin better
    But it makes it harder to read
    """

    # just use a random view
    VIEW_NAME = WriteUpResourceEndpoints.GENERATED_SENTENCE
    VIEW_NEEDS_LOGIN = False

    def setUp(self):
        self.registered_user = User.objects.get(id=self.registered_user_id)
        self.registered_user_client = APIClient()
        self.registered_user_client.force_login(self.registered_user)

        self.staff_user = UserFactory(is_staff=True)
        self.staff_user_client = APIClient()
        self.staff_user_client.force_login(self.staff_user)

    @classmethod
    def set_reversed_url(cls):
        # make this a method so that it can be overriden
        # for any specific urls
        cls.url = reverse(cls.VIEW_NAME)

    @classmethod
    def setUpTestData(cls):
        registered_user = UserFactory(is_staff=False)
        cls.registered_user_id = registered_user.id

        staff_user = UserFactory(is_staff=True)
        cls.staff_user_id = staff_user.id

        cls.set_reversed_url()

    def _get_response(self, staff=False):
        if staff:
            client = self.staff_user_client
        else:
            client = self.registered_user_client

        response = client.get(self.url)
        return response

    def _get_response_data(self, staff=False):
        response = self._get_response(staff)
        return response.data

    def test_get_primary_view(self):
        response = self._get_response()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response)

    def test_not_logged_in_user_cannot_access(self):
        if not self.VIEW_NEEDS_LOGIN:
            return

        # create a random client not logged in
        client = APIClient()
        response = client.get(self.url)
        status_code = response.status_code

        # if not logged in should error out
        self.assertEqual(status_code, 403)
