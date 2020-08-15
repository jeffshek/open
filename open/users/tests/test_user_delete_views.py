from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from test_plus import TestCase

from open.users.constants import UserResourceNames
from open.users.factories import UserFactory
from open.users.models import User
from open.utilities.date_and_time import get_utc_now

"""
dpy test users.tests.test_user_delete_views --keepdb
"""

DEMO_TESTING_PASSWORD = "large-potatos"


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
        user_1.set_password(DEMO_TESTING_PASSWORD)
        user_1.save()

        user_2 = UserFactory(password="potato")
        user_2.set_password(DEMO_TESTING_PASSWORD)
        user_2.save()

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

        user_uuid = str(self.user_1.uuid)

        kwargs = {"uuid": user_uuid}
        data = {"password": DEMO_TESTING_PASSWORD, "uuid": user_uuid}

        url = reverse(user_url, kwargs=kwargs)

        response = self.client_1.delete(url, data=data)
        self.assertEqual(response.status_code, 204, response.content)

        check_existence = User.objects.filter(uuid=self.user_1.uuid).exists()
        other_user_still_fine = User.objects.filter(uuid=self.user_2.uuid).exists()

        self.assertFalse(check_existence)
        self.assertTrue(other_user_still_fine)

    def test_delete_user_view_wrong_password(self):
        user_url = f"users:{UserResourceNames.DELETE_USER_CONFIRMED}"

        user_uuid = str(self.user_1.uuid)

        kwargs = {"uuid": user_uuid}
        data = {"password": "no", "uuid": user_uuid}

        url = reverse(user_url, kwargs=kwargs)

        response = self.client_1.delete(url, data=data)
        self.assertEqual(response.status_code, 400, response.content)

    def test_delete_user_cannot_delete_other_users_with_url_kwargs(self):
        user_url = f"users:{UserResourceNames.DELETE_USER_CONFIRMED}"

        user_uuid = str(self.user_2.uuid)
        kwargs = {"uuid": user_uuid}

        user_2_uuid = str(self.user_2.uuid)
        data = {"password": DEMO_TESTING_PASSWORD, "uuid": user_2_uuid}

        url = reverse(user_url, kwargs=kwargs)

        response = self.client_1.delete(url, data=data)
        self.assertEqual(response.status_code, 400)

        check_user_1 = User.objects.filter(uuid=self.user_1.uuid).exists()
        check_user_2 = User.objects.filter(uuid=self.user_2.uuid).exists()

        self.assertTrue(check_user_1)
        self.assertTrue(check_user_2)

    def test_delete_user_cannot_delete_other_users_with_bad_data(self):
        user_url = f"users:{UserResourceNames.DELETE_USER_CONFIRMED}"

        # if client 1 tried to delete client 2 by specifying in the data response another uuid
        user_1_uuid = str(self.user_1.uuid)
        kwargs = {"uuid": user_1_uuid}

        user_2_uuid = str(self.user_2.uuid)
        data = {"password": DEMO_TESTING_PASSWORD, "uuid": user_2_uuid}

        url = reverse(user_url, kwargs=kwargs)

        response = self.client_1.delete(url, data=data)
        self.assertEqual(response.status_code, 400)

        check_user_1 = User.objects.filter(uuid=self.user_1.uuid).exists()
        check_user_2 = User.objects.filter(uuid=self.user_2.uuid).exists()

        self.assertTrue(check_user_1)
        self.assertTrue(check_user_2)
