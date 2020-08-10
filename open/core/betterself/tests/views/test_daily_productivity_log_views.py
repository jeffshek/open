from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants, TEST_CONSTANTS
from open.core.betterself.factories import DailyProductivityLogFactory
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)
from open.utilities.date_and_time import get_utc_time_relative_units_ago

User = get_user_model()

"""
python manage.py test --pattern="*test_daily_productivity_log_views.py" --keepdb
"""


class DailyProductivityLogTestView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.DAILY_PRODUCTIVITY_LOGS
    model_class_factory = DailyProductivityLogFactory
    model_class = DailyProductivityLog

    def test_create_view(self):
        one_week_ago = get_utc_time_relative_units_ago(weeks=1)
        week_ago_isoformat = one_week_ago.date().isoformat()

        post_data = {
            "very_productive_time_minutes": 10,
            "date": week_ago_isoformat,
            "notes": TEST_CONSTANTS.NOTES_3,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        field_value = data["very_productive_time_minutes"]
        self.assertEqual(field_value, 10)

        field_value = data["notes"]
        self.assertEqual(field_value, TEST_CONSTANTS.NOTES_3)

    def test_create_view_with_just_pomodoros(self):
        one_week_ago = get_utc_time_relative_units_ago(weeks=1)
        week_ago_isoformat = one_week_ago.date().isoformat()

        post_data = {
            "pomodoro_count": 10,
            "date": week_ago_isoformat,
            "notes": TEST_CONSTANTS.NOTES_3,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        field_value = data["pomodoro_count"]
        self.assertEqual(field_value, 10)

        data = response.data
        field_value = data["very_productive_time_minutes"]
        self.assertEqual(field_value, None)

        field_value = data["notes"]
        self.assertEqual(field_value, TEST_CONSTANTS.NOTES_3)

    def test_create_view_with_conflicting_time(self):
        one_week_ago = get_utc_time_relative_units_ago(weeks=1)
        week_ago_isoformat = one_week_ago.date().isoformat()

        post_data = {
            "very_productive_time_minutes": 10,
            "date": week_ago_isoformat,
            "notes": TEST_CONSTANTS.NOTES_3,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        # post again, don't let you create something already made
        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)

        data = response.data
        expected_error_found = "non_field_errors" in data
        self.assertTrue(expected_error_found)


class DailyProductivityLogTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.DAILY_PRODUCTIVITY_LOGS
    model_class_factory = DailyProductivityLogFactory
    model_class = DailyProductivityLog

    def test_update_view_for_new_productivity(self):
        # create an instance already saved
        instance = self.model_class_factory(
            user=self.user_1, very_productive_time_minutes=300, neutral_time_minutes=10
        )
        url = instance.get_update_url()

        params = {"neutral_time_minutes": 20}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        self.assertEqual(data["neutral_time_minutes"], 20)
        self.assertEqual(data["very_productive_time_minutes"], 300)
