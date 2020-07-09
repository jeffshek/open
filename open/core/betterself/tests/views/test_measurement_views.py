from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import MeasurementFactory
from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_measurement_views.py" --keepdb
"""


class TestMeasurementView(TestCase):
    url_name = BetterSelfResourceConstants.MEASUREMENTS
    model_class_factory = MeasurementFactory

    @classmethod
    def setUpClass(cls):
        cls.url = reverse(cls.url_name)
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        user_1 = UserFactory()
        cls.user_1_id = user_1.id

        super().setUpTestData()

    def setUp(self):
        self.user_1 = User.objects.get(id=self.user_1_id)
        self.client_1 = APIClient()
        self.client_1.force_login(self.user_1)

    def test_view(self):
        name = "FOO"
        self.model_class_factory(name=name)

        data = self.client_1.get(self.url).data
        datum = data[0]

        self.assertEqual(len(data), 1)
        self.assertEqual(datum["name"], name)
