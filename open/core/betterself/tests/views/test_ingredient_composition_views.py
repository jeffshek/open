from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    MeasurementFactory,
    IngredientCompositionFactory,
    IngredientFactory,
)
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_ingredient_composition_views.py" --keepdb
"""


class TestIngredientCompositionView(TestCase):
    url_name = BetterSelfResourceConstants.INGREDIENT_COMPOSITIONS
    model_class_factory = IngredientCompositionFactory
    model_class = IngredientComposition

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
        self.model_class.objects.count()
        self.model_class_factory.create_batch(5, user=self.user_1)

        data = self.client_1.get(self.url).data
        self.assertEqual(len(data), 5)

    def test_no_access_view(self):
        self.model_class_factory(user=self.user_1)

        data = self.client_2.get(self.url).data
        self.assertEqual(len(data), 0)

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


class TestIngredientCompositionGetUpdateDelete(TestCase):
    url_name = BetterSelfResourceConstants.INGREDIENT_COMPOSITIONS
    model_class_factory = IngredientCompositionFactory
    model_class = IngredientComposition

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

        self.assertEqual(float(data["quantity"]), instance.quantity)

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
