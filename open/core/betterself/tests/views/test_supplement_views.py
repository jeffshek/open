from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from open.core.betterself.constants import (
    BetterSelfResourceConstants,
    BetterSelfTestContants as CONSTANTS,
)
from open.core.betterself.factories import (
    SupplementFactory,
    IngredientCompositionFactory,
)
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.utilities.serializer_utilties import iterable_to_uuids_list
from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_supplement_views.py" --keepdb
"""


class TestSupplementsView(TestCase):
    url_name = BetterSelfResourceConstants.SUPPLEMENTS
    model_class_factory = SupplementFactory
    model_class = Supplement

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
        post_data = {"name": CONSTANTS.NAME_1, "notes": CONSTANTS.NOTES_1}

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data

        self.assertEqual(data["name"], CONSTANTS.NAME_1)
        self.assertEqual(data["notes"], CONSTANTS.NOTES_1)

    def test_create_view_with_ingredient_compositions(self):
        ind_comps = IngredientCompositionFactory.create_batch(3, user=self.user_1)
        ingredient_composition_uuids = iterable_to_uuids_list(ind_comps)

        post_data = {
            "name": CONSTANTS.NOTES_1,
            "notes": CONSTANTS.NOTES_1,
            "ingredient_composition_uuids": ingredient_composition_uuids,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

    def test_create_view_with_conflicting_ingredient_compositions(self):
        post_data = {
            "name": CONSTANTS.NOTES_1,
            "notes": CONSTANTS.NOTES_1,
            "ingredient_composition_uuids": [CONSTANTS.INVALID_UUID],
        }

        response = self.client_1.post(self.url, data=post_data)

        # error out and say the reason is
        self.assertEqual(response.status_code, 400, response.data)
        self.assertIn("ingredient_composition_uuids", response.data)

    class TestSupplementGetUpdateDelete(TestCase):
        url_name = BetterSelfResourceConstants.INGREDIENT_COMPOSITIONS
        model_class_factory = SupplementFactory
        model_class = Supplement

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
