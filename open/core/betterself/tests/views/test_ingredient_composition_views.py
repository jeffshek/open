from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    MeasurementFactory,
    IngredientCompositionFactory,
    IngredientFactory,
)
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    DeleteTestsMixin,
    GetTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_ingredient_composition_views.py" --keepdb
"""


class TestIngredientCompositionView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.INGREDIENT_COMPOSITIONS
    model_class_factory = IngredientCompositionFactory
    model_class = IngredientComposition

    def test_create_view(self):
        ingredient = IngredientFactory(user=self.user_1)
        measurement = MeasurementFactory()

        post_data = {
            "ingredient_uuid": str(ingredient.uuid),
            "measurement_uuid": str(measurement.uuid),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        ingredient_name = data["ingredient"]["name"]
        self.assertEqual(ingredient.name, ingredient_name)

    def test_create_view_with_bad_ingredient(self):
        ingredient = IngredientFactory(user=self.user_1)
        measurement = MeasurementFactory()

        post_data = {
            "ingredient_uuid": str(measurement.uuid),
            "measurement_uuid": str(measurement.uuid),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)

        post_data = {
            "ingredient_uuid": str(ingredient.uuid),
            "measurement_uuid": str(ingredient.uuid),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_view_with_conflicting_uniqueness(self):
        ingredient = IngredientFactory(user=self.user_1)
        measurement = MeasurementFactory()

        post_data = {
            "ingredient_uuid": str(ingredient.uuid),
            "measurement_uuid": str(measurement.uuid),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

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


class TestIngredientCompositionGetUpdateDelete(
    BetterSelfResourceViewTestCaseMixin, DeleteTestsMixin, GetTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.INGREDIENT_COMPOSITIONS
    model_class_factory = IngredientCompositionFactory
    model_class = IngredientComposition

    def test_update_view_for_quantities(self):
        instance = self.model_class_factory(quantity=10, user=self.user_1,)
        url = instance.get_update_url()

        params = {"quantity": 20}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(float(data["quantity"]), 20, data)

    def test_update_view_for_ingredient(self):
        instance = self.model_class_factory(user=self.user_1,)
        url = instance.get_update_url()

        ingredient = IngredientFactory(user=self.user_1)
        ingredient_uuid = str(ingredient.uuid)

        params = {"ingredient_uuid": ingredient_uuid}
        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(data["ingredient"]["uuid"], ingredient_uuid)

    def test_update_view_with_bad_data(self):
        """ This won't update with an incorrect alternative user """
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        no_permission_ingredient = IngredientFactory(user=self.user_2)
        no_permission_ingredient_uuid = str(no_permission_ingredient.uuid)

        params = {"ingredient_uuid": no_permission_ingredient_uuid}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 400)
        self.assertIn("ingredient_uuid", data)
