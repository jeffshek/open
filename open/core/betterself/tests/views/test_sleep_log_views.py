from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import SleepLogFactory
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.serializers.sleep_log_serializers import (
    SleepLogCreateUpdateSerializer,
)
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)
from open.utilities.date_and_time import (
    get_utc_now,
    get_time_relative_units_forward,
    get_time_relative_units_ago,
    parse_datetime_string,
)
from open.utilities.testing import create_api_request_context

User = get_user_model()

"""
python manage.py test --pattern="*test_sleep_log_views.py" --keepdb
"""


class SleepLogTestView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.SLEEP_LOGS
    model_class_factory = SleepLogFactory
    model_class = SleepLog

    def test_create_view(self):
        end_time = get_utc_now()
        start_time = get_time_relative_units_ago(end_time, hours=8)

        post_data = {"start_time": start_time, "end_time": end_time}

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        value_name = data["end_time"]
        value_parsed = parse_datetime_string(value_name)
        self.assertEqual(end_time, value_parsed)

    def test_create_view_with_blank_notes(self):
        end_time = get_utc_now()
        start_time = get_time_relative_units_ago(end_time, hours=8)

        # important: notes has to have a space when failing with api client!
        post_data = {"start_time": start_time, "end_time": end_time, "notes": " "}

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

    def test_create_serializer_with_no_notes(self):
        """
        This is a REALLY weird problem where requests not originating from tests are failing when blank is left empty
        """
        end_time = get_utc_now()
        start_time = get_time_relative_units_ago(end_time, hours=8)

        # empty string with notes here will still fail if it's broken -- this is with an RequestFactory
        # to mimic how data is sent, i think APIClient serializes something
        post_data = {"start_time": start_time, "end_time": end_time, "notes": ""}

        context = create_api_request_context(self.url, self.user_1, post_data)

        serializer = SleepLogCreateUpdateSerializer(data=post_data, context=context)
        valid = serializer.is_valid()

        self.assertTrue(valid, serializer.errors)

    def test_create_view_with_nonsensical_start_time(self):
        end_time = get_utc_now()
        # get 8 hours in advance
        start_time = get_time_relative_units_forward(end_time, hours=8)

        post_data = {"start_time": start_time, "end_time": end_time}

        response = self.client_1.post(self.url, data=post_data)

        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue("non_field_errors" in response.data)

    def test_create_view_with_conflicting_unique(self):
        end_time = get_utc_now()
        start_time = get_time_relative_units_ago(end_time, hours=8)

        post_data = {"start_time": start_time, "end_time": end_time}

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        value_name = data["end_time"]
        value_parsed = parse_datetime_string(value_name)
        self.assertEqual(end_time, value_parsed)

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


class SleepLogTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.SLEEP_LOGS
    model_class_factory = SleepLogFactory
    model_class = SleepLog

    def test_avoid_extra_sql_queries(self):
        # even if we create a bunch of data, when fetching, it shouldn't result in a lot of n+1 queries
        self.model_class_factory.create_batch(10, user=self.user_1)
        with self.assertNumQueriesLessThan(6):
            self.client_1.get(self.url)

    def test_update_view_for_new_activity(self):
        # create an instance already saved
        instance = SleepLogFactory(user=self.user_1)
        url = instance.get_update_url()

        end_time = get_utc_now()
        params = {"end_time": end_time}

        response = self.client_1.post(url, data=params)
        data = response.data

        self.assertEqual(response.status_code, 200, data)
        end_time_parsed = parse_datetime_string(data["end_time"])
        self.assertEqual(end_time_parsed, end_time)
