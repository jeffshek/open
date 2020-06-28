from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test core.betterself --pattern="*test_views.py"
"""


class TestFactoryCreation(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.default_user = UserFactory()
        super().setUpTestData()

    def setUp(self):
        self.client = APIClient()
        self.client.force_login(self.default_user)

    def test_view(self):
        # just in mock phase
        return
