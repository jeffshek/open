from dateutil import relativedelta
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    SleepLogFactory,
    SupplementFactory,
    SupplementLogFactory,
    DailyProductivityLogFactory,
    FoodLogFactory,
    WellBeingLogFactory,
)
from open.core.betterself.tests.mixins.resource_mixin import BaseTestCase
from open.users.factories import UserFactory
from open.utilities.date_and_time import (
    get_utc_now,
    yyyy_mm_dd_format_1,
    get_today_formatted_api_format,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_daily_review_view.py" --keepdb
"""


class DailyReviewViewTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = UserFactory()
        user_2 = UserFactory()

        cls.end_period = get_utc_now()
        cls.end_period_date_string = cls.end_period.date().strftime(yyyy_mm_dd_format_1)

        supplements = SupplementFactory.create_batch(2, user=user_1)

        for index in range(3):
            # simulate some missing data
            if index % 5 == 0 and index != 0:
                continue

            date_to_use = cls.end_period - relativedelta.relativedelta(days=index)
            SleepLogFactory(end_time=date_to_use, user=user_1)

            for supplement in supplements:
                SupplementLogFactory.create_batch(
                    10, user=user_1, supplement=supplement, time=date_to_use
                )

        cls.user_1_id = user_1.id
        cls.user_2_id = user_2.id

        for index in range(3):
            # simulate some missing data
            if index % 5 == 0 and index != 0:
                continue

            date_to_use = cls.end_period - relativedelta.relativedelta(days=index)
            DailyProductivityLogFactory(user=user_1, date=date_to_use)

            # add some random data to user_2 also to make sure no leaking
            DailyProductivityLogFactory(user=user_2, date=date_to_use)

            FoodLogFactory.create_batch(10, user=user_1, time=date_to_use)
            WellBeingLogFactory.create_batch(10, user=user_1, time=date_to_use)

    def test_url(self):
        kwargs = {"date": get_today_formatted_api_format()}
        url = reverse(BetterSelfResourceConstants.DAILY_REVIEW, kwargs=kwargs)
        self.assertIsNotNone(url)

    def test_view(self):
        kwargs = {"date": get_today_formatted_api_format()}
        url = reverse(BetterSelfResourceConstants.DAILY_REVIEW, kwargs=kwargs)

        response = self.client_1.get(url)
        data = response.data
        self.assertEqual(response.status_code, 200, data)

    def test_sql_query_count(self):
        kwargs = {"date": get_today_formatted_api_format()}
        url = reverse(BetterSelfResourceConstants.DAILY_REVIEW, kwargs=kwargs)

        with self.assertNumQueriesLessThan(20):
            self.client_1.get(url)
