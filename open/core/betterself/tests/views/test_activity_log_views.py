from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import (
    BetterSelfResourceConstants,
    TEST_CONSTANTS,
)
from open.core.betterself.factories import ActivityFactory, ActivityLogFactory
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_activity_log_views.py" --keepdb
"""


class ActivityLogTestView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.ACTIVITY_LOGS
    model_class_factory = ActivityLogFactory
    model_class = ActivityLog

    def test_create_view(self):
        activity = ActivityFactory(name=TEST_CONSTANTS.NAME_1, user=self.user_1)

        post_data = {
            "activity_uuid": str(activity.uuid),
            "time": self.current_time_isoformat,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        value_name = data["activity"]["name"]
        self.assertEqual(TEST_CONSTANTS.NAME_1, value_name)

    def test_create_view_with_bad_activity_no_permission(self):
        activity = ActivityFactory(name=TEST_CONSTANTS.NAME_1, user=self.user_2)

        post_data = {
            "activity_uuid": str(activity.uuid),
            "time": self.current_time_isoformat,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_view_with_conflicting_unique(self):
        activity = ActivityFactory(name=TEST_CONSTANTS.NAME_1, user=self.user_1)

        post_data = {
            "activity_uuid": str(activity.uuid),
            "time": self.current_time_isoformat,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200)

        # post again, don't let you create something already made
        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)

        data = response.data
        """
        error_message should be
        {'non_field_errors': [ErrorDetail(string='The fields user, name must make a unique set.', code='unique')]}
        """
        expected_error_found = "non_field_errors" in data
        self.assertTrue(expected_error_found)


class ActivityLogTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.ACTIVITY_LOGS
    model_class_factory = ActivityLogFactory
    model_class = ActivityLog

    def test_update_view_for_new_activity(self):
        # create an instance already saved
        instance = ActivityLogFactory(user=self.user_1)

        update_parameter = ActivityFactory(user=self.user_1)
        update_uuid = str(update_parameter.uuid)
        url = instance.get_update_url()

        params = {"activity_uuid": update_uuid}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(data["activity"]["uuid"], update_uuid)

    def test_update_view_for_new_activity_but_no_access(self):
        # create an instance already saved
        instance = ActivityLogFactory(user=self.user_1)

        update_parameter = ActivityFactory(user=self.user_2)
        update_uuid = str(update_parameter.uuid)
        url = instance.get_update_url()

        params = {"activity_uuid": update_uuid}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 400, data)
        self.assertTrue("activity_uuid" in response.data)
