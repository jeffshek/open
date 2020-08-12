from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from test_plus import TestCase

from open.users.constants import UserResourceNames
from open.users.factories import UserFactory
from open.users.models import User
from open.utilities.date_and_time import get_utc_now

"""
dpy test users.tests.test_user_delete_views
"""


class TestUserDeleteView(TestCase):
    url_name = "users:" + UserResourceNames.DETAILS
    model_class = User
    model_class_factory = UserFactory

    @classmethod
    def setUpClass(cls):
        cls.url = reverse(cls.url_name)

        cls.current_time = get_utc_now()
        cls.current_time_isoformat = cls.current_time.isoformat()

        cls.current_date = cls.current_time.date()
        cls.current_date_isoformat = cls.current_date.isoformat()

        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        user_1 = UserFactory()
        user_2 = UserFactory()

        cls.user_1_id = user_1.id
        cls.user_2_id = user_2.id

        super().setUpTestData()

    def setUp(self):
        self.user_1 = User.objects.get(id=self.user_1_id)
        self.user_2 = User.objects.get(id=self.user_2_id)

        # a user that owns the instance
        self.client_1 = APIClient()
        self.client_1.force_login(self.user_1)

        # a user that shouldn't have access to the instance
        self.client_2 = APIClient()
        self.client_2.force_login(self.user_2)

        super().setUp()

    def test_delete_user_view(self):
        user_url = f"users:{UserResourceNames.DELETE_USER_CONFIRMED}"

        kwargs = {"uuid": str(self.user_1.uuid)}
        url = reverse(user_url, kwargs=kwargs)

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, 204)

        check_existence = User.objects.filter(uuid=self.user_1.uuid).exists()
        other_user_still_fine = User.objects.filter(uuid=self.user_2.uuid).exists()

        self.assertFalse(check_existence)
        self.assertTrue(other_user_still_fine)

    def test_delete_user_cannot_delete_other_users(self):
        user_url = f"users:{UserResourceNames.DELETE_USER_CONFIRMED}"

        kwargs = {"uuid": str(self.user_2.uuid)}
        url = reverse(user_url, kwargs=kwargs)

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, 404)

        check_user_1 = User.objects.filter(uuid=self.user_1.uuid).exists()
        check_user_2 = User.objects.filter(uuid=self.user_2.uuid).exists()

        self.assertTrue(check_user_1)
        self.assertTrue(check_user_2)
