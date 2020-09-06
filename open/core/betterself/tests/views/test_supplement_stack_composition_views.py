from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    SupplementStackCompositionFactory,
    SupplementStackFactory,
    SupplementFactory,
)
from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_supplement_stack_composition_views.py" --keepdb
"""


class SupplementStackCompositionCreateTestView(
    BetterSelfResourceViewTestCaseMixin, TestCase
):
    url_name = BetterSelfResourceConstants.SUPPLEMENT_STACK_COMPOSITIONS
    model_class_factory = SupplementStackCompositionFactory
    model_class = SupplementStackComposition

    def test_create_view(self):
        supplement = SupplementFactory(user=self.user_1)
        stack = SupplementStackFactory(user=self.user_1)

        supplement_uuid = str(supplement.uuid)
        stack_uuid = str(stack.uuid)
        quantity = 5

        post_data = {
            "supplement_uuid": supplement_uuid,
            "stack_uuid": stack_uuid,
            "quantity": quantity,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)

    def test_create_view_with_duplication_data(self):
        supplement = SupplementFactory(user=self.user_1)
        stack = SupplementStackFactory(user=self.user_1)

        supplement_uuid = str(supplement.uuid)
        stack_uuid = str(stack.uuid)
        quantity = 5

        post_data = {
            "supplement_uuid": supplement_uuid,
            "stack_uuid": stack_uuid,
            "quantity": quantity,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400)

        expected_error_found = "non_field_errors" in response.data
        self.assertTrue(expected_error_found)


class SupplementStackCompositionTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.SUPPLEMENT_STACK_COMPOSITIONS
    model_class_factory = SupplementStackCompositionFactory
    model_class = SupplementStackComposition

    def test_update_quantity_in_supplement_stack_composition(self):
        instance = SupplementStackCompositionFactory(user=self.user_1, quantity=10)

        url = instance.get_update_url()
        params = {"uuid": str(instance.uuid), "quantity": 5}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(float(data["quantity"]), 5)

    def test_update_supplement_in_supplement_stack_composition(self):
        instance = SupplementStackCompositionFactory(user=self.user_1, quantity=10)

        supplement = SupplementFactory(user=self.user_1)

        self.assertNotEqual(instance.supplement, supplement)

        url = instance.get_update_url()
        params = {"supplement_uuid": str(supplement.uuid), "quantity": 5}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(data["supplement"]["uuid"], str(supplement.uuid))
