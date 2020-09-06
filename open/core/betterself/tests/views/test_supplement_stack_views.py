from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import SupplementStackFactory
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_supplement_stack_views.py" --keepdb
"""


class SupplementStackCreateTestView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.SUPPLEMENT_STACKS
    model_class_factory = SupplementStackFactory
    model_class = SupplementStack

    def test_create_view(self):
        silly_name = "MENTAL FOCUS POWER"
        post_data = {"name": silly_name}

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)

        data = response.data
        self.assertEqual(data["name"], silly_name)


class SupplementStackTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.SUPPLEMENT_STACKS
    model_class_factory = SupplementStackFactory
    model_class = SupplementStack

    def test_update_stack_name(self):
        stack = SupplementStackFactory(user=self.user_1)
        cool_name = "cool name"

        params = {"name": cool_name}
        url = stack.get_update_url()

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(data["name"], cool_name)

    def test_update_stack_name_no_access(self):
        stack = SupplementStackFactory(user=self.user_1)
        cool_name = "cool name"

        params = {"name": cool_name}
        url = stack.get_update_url()

        # use a different client to make sure no data
        response = self.client_2.post(url, data=params)
        self.assertEqual(404, response.status_code)
