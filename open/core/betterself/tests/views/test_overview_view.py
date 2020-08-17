import datetime

from dateutil import relativedelta
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    SleepLogFactory,
    SupplementFactory,
    SupplementLogFactory,
)
from open.core.betterself.tests.mixins.resource_mixin import BaseTestCase
from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_overview_view.py" --keepdb

dpy test open.core.betterself.tests.views.test_overview_view.OverviewTestView.test_view_response --keepdb
"""


class OverviewTestView(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = UserFactory()
        user_2 = UserFactory()

        # do 2 days ago, that way you can create data faster when self-testing
        start_period = datetime.datetime(2020, 9, 22, tzinfo=user_1.timezone)

        supplements = SupplementFactory.create_batch(2, user=user_1)

        for index in range(3):
            date_to_use = start_period - relativedelta.relativedelta(days=index)
            SleepLogFactory(end_time=date_to_use, user=user_1)

            for supplement in supplements:
                SupplementLogFactory.create_batch(
                    2, user=user_1, supplement=supplement, time=date_to_use
                )

        cls.user_1_id = user_1.id
        cls.user_2_id = user_2.id

    def test_url(self):
        kwargs = {"period": "monthly", "date": "2020-08-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)
        self.assertIsNotNone(url)

    def test_view(self):
        kwargs = {"period": "monthly", "date": "2020-08-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 200, response.data)

    def test_view_invalid_date(self):
        kwargs = {"period": "monthly", "date": "2020-999-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 404, response.data)

    def test_view_weekly(self):
        kwargs = {"period": "weekly", "date": "2020-10-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 200, response.data)

    def test_view_response(self):
        start_period = "2020-08-22"
        kwargs = {"period": "monthly", "date": start_period}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

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
        start_period = "2020-08-22"
        kwargs = {"period": "monthly", "date": start_period}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

        data = self.client_1.get(url).data
        supplements_data = data["supplements"]

        import pprint

        pprint.pprint(supplements_data)

    def test_view_response_with_no_data(self):
        start_period = "2020-08-22"
        kwargs = {"period": "monthly", "date": start_period}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

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
