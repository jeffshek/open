from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import IngredientFactory
from open.core.betterself.models.ingredient import Ingredient
from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_ingredient_views.py" --keepdb
"""


class TestIngredientCreateListView(TestCase):
    url_name = BetterSelfResourceConstants.INGREDIENTS
    model_class_factory = IngredientFactory
    model_class = Ingredient

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

        # create a few instances that will never be used
        cls.model_class_factory.create_batch(5)

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
        names_to_create = ["a", "b", "c", "d", "e", "f"]
        for name in names_to_create:
            self.model_class_factory.create(name=name, user=self.user_1)

        # create_batch = 5
        # self.model_class_factory.create_batch(create_batch, user=self.user_1)

        data = self.client_1.get(self.url).data
        datum = data[0]

        self.assertEqual(len(data), 6)
        self.assertTrue(datum["name"] in names_to_create)

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
        post_data = {
            "name": "name",
            "notes": "notes1",
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        self.assertEqual(data["notes"], "notes1")

        post_data = {
            "name": "name",
            "notes": "notes2",
        }

        # don't let you recreate something that already's been made
        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)

        data = response.data
        """
        error_message should be
        {'non_field_errors': [ErrorDetail(string='The fields user, name must make a unique set.', code='unique')]}
        """
        expected_error_found = "non_field_errors" in data
        self.assertTrue(expected_error_found)


class TestIngredientGetUpdateDelete(TestCase):
    url_name = BetterSelfResourceConstants.INGREDIENTS
    model_class_factory = IngredientFactory
    model_class = Ingredient

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

        # create a few instances that will never be used
        cls.model_class_factory.create_batch(5)

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

    def test_get_singular_resource(self):
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        response = self.client_1.get(url)
        data = response.data

        self.assertEqual(data["name"], instance.name)

    def test_delete_view_on_non_uuid_url(self):
        response = self.client_1.delete(self.url)
        self.assertEqual(response.status_code, 405, response.data)

    def test_delete_view(self):
        instance = self.model_class_factory(user=self.user_1)
        instance_id = instance.id

        url = instance.get_update_url()

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, 204, response.data)

        with self.assertRaises(ObjectDoesNotExist):
            self.model_class.objects.get(id=instance_id)

    def test_update_view(self):
        original_name = "FOO"
        original_notes = "okay"
        revised_notes = "revised"

        instance = self.model_class_factory(
            name=original_name, user=self.user_1, notes=original_notes
        )
        url = instance.get_update_url()

        params = {"notes": revised_notes}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(data["name"], original_name, data)
        self.assertEqual(data["notes"], revised_notes, data)

    def test_update_view_with_bad_data(self):
        """ This won't update even if you try to use an alternative user """
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        params = {"user": self.user_2}

        response = self.client_1.post(url, data=params)
        self.assertEqual(response.data["user"]["uuid"], str(self.user_1.uuid))

    def test_update_view_with_invalid_user_permission(self):
        """
        No one should be able to access other people's data
        """
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        params = {"notes": "fake spoof"}

        response = self.client_2.post(url, data=params)
        self.assertEqual(response.status_code, 404, response.data)
