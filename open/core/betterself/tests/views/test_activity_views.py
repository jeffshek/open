from django.contrib.auth import get_user_model
from django.test import TestCase

from open.core.betterself.constants import (
    BetterSelfResourceConstants,
    BetterSelfTestContants,
)
from open.core.betterself.factories import ActivityFactory
from open.core.betterself.models.activity import Activity
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_activity_views.py" --keepdb
"""


class TestActivityView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.ACTIVITIES
    model_class_factory = ActivityFactory
    model_class = Activity

    def test_create_view(self):
        post_data = {
            "name": BetterSelfTestContants.NAME_1,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        value_name = data["name"]
        self.assertEqual(BetterSelfTestContants.NAME_1, value_name)

    def test_create_view_with_conflicting_uniqueness(self):
        post_data = {
            "name": BetterSelfTestContants.NAME_1,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

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
    BetterSelfResourceViewTestCaseMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.ACTIVITIES
    model_class_factory = ActivityFactory
    model_class = Activity

    def test_get_singular_resource(self):
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        response = self.client_1.get(url)
        data = response.data

        for key, value in data.items():
            instance_value = getattr(instance, key)
            if isinstance(instance_value, (str, bool)):
                # if the field stored on the db level is the right noe
                self.assertEqual(instance_value, value)

    def test_update_view_for_name(self):
        instance = self.model_class_factory(
            user=self.user_1, name=BetterSelfTestContants.NAME_2
        )
        url = instance.get_update_url()

        params = {"name": BetterSelfTestContants.NAME_1}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(data["name"], BetterSelfTestContants.NAME_1, data)

    def test_update_view_with_invalid_user_permission(self):
        """
        No one should be able to access other people's data
        """
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        params = {"notes": "fake spoof"}

        response = self.client_2.post(url, data=params)
        self.assertEqual(response.status_code, 404, response.data)
