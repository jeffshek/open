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

    def test_create_view(self):
        post_data = {
            "name": "name",
            "notes": "notes",
        }
        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        self.assertEqual(data["name"], "name")

    def test_create_view_with_conflicting_uniqueness(self):
        """
        I don't know if I like this yet, I'm allowing multiple
        create attempts to not have a conflict and to simply override
        the data ...

        Actually nevermind, I don't like this. It allows someone to overwrite
        valuable notes by accident - for instance, if someone creates the same
        ingredient twice by accident, and they have data in some non-required field,
        poof it goes back to blank. That would be bad.
        """
        post_data = {
            "name": "name",
            "notes": "notes1",
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        uuid_response = data["uuid"]
        self.assertEqual(data["notes"], "notes1")

        post_data = {
            "name": "name",
            "notes": "notes2",
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        self.assertEqual(data["notes"], "notes1")
        # uuid should be the same if we're sending the same data
        self.assertEqual(data["uuid"], uuid_response)

    def test_delete_view(self):
        return

    def test_update_view(self):
        name = "FOO"
        self.model_class_factory(name=name, user=self.user_1)
        return
