from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from open.core.views import SENTENCE_1_MOCK_RESPONSE
from open.core.writeup.constants import WriteUpResourceEndpoints
from open.users.factories import UserFactory

User = get_user_model()


class TestGeneratedStringView(TestCase):
    URL = reverse(WriteUpResourceEndpoints.GENERATED_SENTENCE)

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
        response = self.client.get(self.URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["sentence1"], SENTENCE_1_MOCK_RESPONSE)
