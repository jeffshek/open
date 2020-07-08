from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import IngredientFactory
from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_ingredient_views.py" --keepdb
"""


class TestIngredientView(TestCase):
    url_name = BetterSelfResourceConstants.INGREDIENTS
    model_class_factory = IngredientFactory

    @classmethod
    def setUpClass(cls):
        cls.url = reverse(cls.url_name)
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

    def test_view(self):
        name = "FOO"
        self.model_class_factory(name=name, user=self.user_1)

        data = self.client_1.get(self.url).data
        datum = data[0]

        self.assertEqual(len(data), 1)
        self.assertEqual(datum["name"], name)

    def test_no_access_view(self):
        name = "FOO"
        self.model_class_factory(name=name, user=self.user_1)

        data = self.client_2.get(self.url).data
        self.assertEqual(len(data), 0)

    def test_update_view(self):
        name = "FOO"
        self.model_class_factory(name=name, user=self.user_1)
        return

    def test_create_view(self):
        return

    def test_delete_view(self):
        return
