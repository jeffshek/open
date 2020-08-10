from django.contrib.auth import get_user_model
from test_plus import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_user_details_view.py" --keepdb
"""


class TestUserDetailsView(TestCase):
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

    def test_view(self):
        url = reverse("users:details")

        response = self.client_1.get(url)
        data = response.data

        self.assertEqual(data["username"], self.user_1.username)
