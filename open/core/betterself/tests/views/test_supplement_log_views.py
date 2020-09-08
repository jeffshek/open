from django.contrib.auth import get_user_model

from test_plus import TestCase

from open.core.betterself.constants import (
    BetterSelfResourceConstants,
    TEST_CONSTANTS,
)
from open.core.betterself.factories import (
    SupplementLogFactory,
    SupplementFactory,
    SupplementStackFactory,
    SupplementStackCompositionFactory,
)
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    DeleteTestsMixin,
    GetTestsMixin,
)
from open.utilities.date_and_time import (
    get_utc_now,
    get_time_relative_units_ago,
    get_time_relative_units_forward,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_supplement_log_views.py" --keepdb
dpy test open.core.betterself.tests.views.test_supplement_log_views.TestSupplementLogViews --keepdb
"""


class TestSupplementLogCreateViews(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.SUPPLEMENT_LOGS
    model_class_factory = SupplementLogFactory
    model_class = SupplementLog

    def test_create_view(self):
        """
        dpy test  open.core.betterself.tests.views.test_supplement_log_views.TestSupplementLogViews.test_create_view --keepdb

        """
        supplement = SupplementFactory(user=self.user_1)
        time = get_utc_now()

        post_data = {
            "supplement_uuid": str(supplement.uuid),
            "time": time.isoformat(),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        supplement_name = data["supplement"]["name"]
        self.assertEqual(supplement.name, supplement_name)
        self.assertIsNotNone(data["display_name"])

    def test_create_view_with_bad_supplement(self):
        time = get_utc_now()

        post_data = {
            "supplement_uuid": TEST_CONSTANTS.INVALID_UUID,
            "time": time.isoformat(),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)

    def test_create_view_with_empty_notes(self):
        supplement = SupplementFactory(user=self.user_1)
        time = get_utc_now()

        post_data = {
            "supplement_uuid": str(supplement.uuid),
            "time": time.isoformat(),
            "quantity": 5,
            "notes": " ",
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

    def test_create_view_with_conflicting_uniqueness(self):
        supplement = SupplementFactory(user=self.user_1)
        time = get_utc_now()

        post_data = {
            "supplement_uuid": str(supplement.uuid),
            "time": time.isoformat(),
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

    def test_display_name_on_log_serializer_some_hours_ago(self):
        """
        dpy test  open.core.betterself.tests.views.test_supplement_log_views.TestSupplementLogViews.test_display_name_on_log_serializer_some_hours_ago --keepdb
        """
        supplement = SupplementFactory(user=self.user_1)
        utc_now = get_utc_now()

        # if you adjust it this way, it should result in about 4.5 hours ago
        time = get_time_relative_units_ago(utc_now, hours=5.0)
        time = get_time_relative_units_forward(time, minutes=30)

        post_data = {
            "supplement_uuid": str(supplement.uuid),
            "time": time.isoformat(),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        display_name = response.data["display_name"]
        self.assertTrue("4.5 hours ago" in display_name, display_name)

    def test_display_name_on_log_serializer_some_days_ago(self):
        supplement = SupplementFactory(user=self.user_1)
        utc_now = get_utc_now()

        time = get_time_relative_units_ago(utc_now, days=8.5)

        post_data = {
            "supplement_uuid": str(supplement.uuid),
            "time": time.isoformat(),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        display_name = response.data["display_name"]
        self.assertTrue("8.5 days ago" in display_name, display_name)

    def test_create_supplement_log_with_supplement_stack(self):
        """
        dpy test open.core.betterself.tests.views.test_supplement_log_views.TestSupplementLogViews.test_create_supplement_log_with_supplement_stack --keepdb
        """
        # a hidden feature, not really restful, but allow a user to send a supplement_stack_uuid
        # to create a set of supplements taken at the same time

        supplements = SupplementFactory.create_batch(3, user=self.user_1)
        stack = SupplementStackFactory(user=self.user_1)

        compositions = []
        for supplement in supplements:
            composition = SupplementStackCompositionFactory(
                user=self.user_1, supplement=supplement, stack=stack, quantity=2
            )
            compositions.append(composition)

        stack_uuid = stack.uuid

        utc_now = get_utc_now()
        post_data = {
            "supplement_uuid": str(stack_uuid),
            "time": utc_now.isoformat(),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        for supplement in supplements:
            matching_log = SupplementLog.objects.get(
                supplement=supplement, quantity=10, user=self.user_1, time=utc_now
            )
            self.assertIsNotNone(matching_log)


class TestSupplementLogGetUpdateDelete(
    BetterSelfResourceViewTestCaseMixin, TestCase, GetTestsMixin, DeleteTestsMixin
):
    url_name = BetterSelfResourceConstants.SUPPLEMENT_LOGS
    model_class_factory = SupplementLogFactory
    model_class = SupplementLog

    def test_edit_supplement_log_with_supplement_stack(self):
        log = SupplementLogFactory.create(user=self.user_1)
        stack = SupplementStackFactory(user=self.user_1)

        update_url = log.get_update_url()

        data = {"supplement_uuid": str(stack.uuid)}

        response = self.client_1.post(update_url, data=data)
        self.assertEqual(response.status_code, 400)
