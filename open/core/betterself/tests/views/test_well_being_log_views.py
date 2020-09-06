from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import WellBeingLogFactory
from open.core.betterself.models.well_being_log import WellBeingLog
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_well_being_log_views.py" --keepdb
"""


class WellBeingLogCreateTestView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.WELL_BEING_LOGS
    model_class_factory = WellBeingLogFactory
    model_class = WellBeingLog

    def test_create_view_with_conflicting_unique(self):
        post_data = {"time": self.current_time_isoformat, "mental_value": 5}

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


class WellBeingLogTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.WELL_BEING_LOGS
    model_class_factory = WellBeingLogFactory
    model_class = WellBeingLog

    def test_update_view_with_updated_params(self):
        instance = self.model_class_factory(user=self.user_1)
        previous_mental_value = instance.mental_value
        url = instance.get_update_url()

        params = {"mental_value": previous_mental_value + 1}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(data["mental_value"], previous_mental_value + 1)

        instance.refresh_from_db()
        self.assertEqual(instance.mental_value, previous_mental_value + 1)
