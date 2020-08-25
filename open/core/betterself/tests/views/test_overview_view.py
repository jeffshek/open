from dateutil import relativedelta
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    SleepLogFactory,
    SupplementFactory,
    SupplementLogFactory,
    DailyProductivityLogFactory,
)
from open.core.betterself.tests.mixins.resource_mixin import BaseTestCase
from open.users.factories import UserFactory
from open.utilities.date_and_time import get_utc_now, yyyy_mm_dd_format_1

User = get_user_model()

"""
python manage.py test --pattern="*test_overview_view.py" --keepdb

dpy test open.core.betterself.tests.views.test_overview_view.OverviewTestView.test_view_response_for_productivity --keepdb
"""


class OverviewTestView(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = UserFactory()
        user_2 = UserFactory()

        # push a month back for the start_period
        # edit not sure why, so i took it off

        cls.end_period = get_utc_now()
        cls.end_period_date_string = cls.end_period.date().strftime(yyyy_mm_dd_format_1)

        supplements = SupplementFactory.create_batch(2, user=user_1)

        for index in range(30):
            # simulate some missing data
            if index % 5 == 0:
                continue

            date_to_use = cls.end_period - relativedelta.relativedelta(days=index)
            SleepLogFactory(end_time=date_to_use, user=user_1)

            for supplement in supplements:
                SupplementLogFactory.create_batch(
                    2, user=user_1, supplement=supplement, time=date_to_use
                )

        cls.user_1_id = user_1.id
        cls.user_2_id = user_2.id

        for index in range(30):
            # simulate some missing data
            if index % 5 == 0:
                continue

            date_to_use = cls.end_period - relativedelta.relativedelta(days=index)
            DailyProductivityLogFactory(user=user_1, date=date_to_use)

            # add some random data to user_2 also to make sure no leaking
            DailyProductivityLogFactory(user=user_2, date=date_to_use)

    def test_url(self):
        kwargs = {"period": "monthly", "date": "2020-08-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)
        self.assertIsNotNone(url)

    def test_view(self):
        kwargs = {"period": "monthly", "date": "2020-08-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)

        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 200, response.data)

    def test_view_invalid_date(self):
        kwargs = {"period": "monthly", "date": "2020-999-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)

        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 404, response.data)

    def test_view_weekly(self):
        kwargs = {"period": "weekly", "date": "2020-10-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)

        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 200, response.data)

    def test_view_response(self):
        start_period = "2020-08-22"
        kwargs = {"period": "monthly", "date": start_period}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)

        data = self.client_1.get(url).data

        expected_keys = ["period", "start_period", "end_period"]
        data_keys = data.keys()

        valid_response = set(expected_keys).issubset(data_keys)
        msg = f"Expected {expected_keys} in {data_keys}"
        self.assertTrue(valid_response, msg=msg)

        data_start_period = data["start_period"]
        data_end_period = data["end_period"]

        self.assertEqual(data_start_period, start_period)
        self.assertNotEqual(data_end_period, start_period)

    def test_view_response_for_supplements(self):
        start_period = self.end_period_date_string
        kwargs = {"period": "monthly", "date": start_period}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)

        data = self.client_1.get(url).data
        supplements_data = data["supplements"]

        # garbage assertion, but i'll write better tests when i can visualize how the frontend
        # should display the data
        self.assertIsNotNone(supplements_data)

    def test_view_response_for_productivity(self):
        start_period = self.end_period_date_string
        kwargs = {"period": "weekly", "date": start_period}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)

        data = self.client_1.get(url).data
        data = data["productivity"]

        # rofl, what a bad test.
        logs = data["logs"]
        self.assertTrue(logs)

    def test_view_response_with_no_data(self):
        start_period = "1998-08-22"

        kwargs = {"period": "monthly", "date": start_period}
        url = reverse(BetterSelfResourceConstants.OVERVIEW, kwargs=kwargs)

        data = self.client_2.get(url).data

        expected_keys = ["period", "start_period", "end_period"]
        data_keys = data.keys()

        valid_response = set(expected_keys).issubset(data_keys)
        msg = f"Expected {expected_keys} in {data_keys}"
        self.assertTrue(valid_response, msg=msg)

        data_start_period = data["start_period"]
        data_end_period = data["end_period"]

        self.assertEqual(data_start_period, start_period)
        self.assertNotEqual(data_end_period, start_period)
