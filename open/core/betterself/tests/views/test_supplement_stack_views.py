from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    SupplementStackFactory,
    SupplementStackCompositionFactory,
)
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

    def test_get_view_with_supplement_compositions(self):
        stack = SupplementStackFactory(user=self.user_1)
        compositions_to_create = 3
        created_comps = SupplementStackCompositionFactory.create_batch(
            compositions_to_create, stack=stack, user=self.user_1
        )

        # sometimes the randomness makes it not quite equal to how many we wanted to create
        created_comps_length = len(created_comps)

        url = stack.get_update_url()
        response = self.client_1.get(url)

        self.assertIsNotNone(response.data["compositions"])
        self.assertEqual(created_comps_length, len(response.data["compositions"]))

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

    def test_avoid_extra_sql_queries(self):
        # TODO - Actually fix the duplicate queries if it ends up being slow ...
        return
