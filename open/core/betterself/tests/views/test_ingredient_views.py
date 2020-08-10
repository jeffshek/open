from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import IngredientFactory
from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_ingredient_views.py" --keepdb
"""


class TestIngredientCreateListView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.INGREDIENTS
    model_class_factory = IngredientFactory
    model_class = Ingredient

    def test_view(self):
        names_to_create = ["a", "b", "c", "d", "e", "f"]
        for name in names_to_create:
            self.model_class_factory.create(name=name, user=self.user_1)

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


class TestIngredientGetUpdateDelete(
    BetterSelfResourceViewTestCaseMixin, TestCase, GetTestsMixin, DeleteTestsMixin
):
    url_name = BetterSelfResourceConstants.INGREDIENTS
    model_class_factory = IngredientFactory
    model_class = Ingredient

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
