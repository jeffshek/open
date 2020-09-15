from dateutil import relativedelta
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import (
    SleepLogFactory,
    SupplementFactory,
    SupplementLogFactory,
    DailyProductivityLogFactory,
    FoodFactory,
    FoodLogFactory,
)
from open.core.betterself.models.food_logs import FoodLog
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.tests.mixins.resource_mixin import BaseTestCase
from open.core.betterself.utilities.user_date_utilities import (
    serialize_date_to_user_localized_datetime,
)
from open.users.factories import UserFactory
from open.utilities.date_and_time import (
    get_utc_now,
    yyyy_mm_dd_format_1,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_aggregrate_views.py" --keepdb
dpy test open.core.betterself.tests.views.test_aggregrate_views.TestAggregateView
"""


class TestAggregateView(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = UserFactory()
        user_2 = UserFactory()

        cls.end_period = get_utc_now()
        cls.end_period_date_string = cls.end_period.date().strftime(yyyy_mm_dd_format_1)

        supplements = SupplementFactory.create_batch(10, user=user_1)

        for index in range(100):
            # simulate some missing data
            if index % 5 == 0 and index != 0:
                continue

            date_to_use = cls.end_period - relativedelta.relativedelta(days=index)
            SleepLogFactory(end_time=date_to_use, user=user_1)

            for supplement in supplements:
                SupplementLogFactory.create_batch(
                    2, user=user_1, supplement=supplement, time=date_to_use
                )

        cls.user_1_id = user_1.id
        cls.user_2_id = user_2.id

        for index in range(100):
            # simulate some missing data
            if index % 5 == 0 and index != 0:
                continue

            date_to_use = cls.end_period - relativedelta.relativedelta(days=index)
            DailyProductivityLogFactory(user=user_1, date=date_to_use)

            # add some random data to user_2 also to make sure no leaking
            DailyProductivityLogFactory(user=user_2, date=date_to_use)

    def test_url(self):
        url = reverse(BetterSelfResourceConstants.AGGREGATE)

        kwargs = {"start_date": "2020-01-02", "end_date": "2020-01-02"}

        response = self.client_1.post(url, data=kwargs)
        self.assertEqual(response.status_code, 200, response.data)

        # nothing in kwargs, should have no supplements data
        self.assertNotIn("supplements", response.data)

    def test_url_with_supplements_requested(self):
        url = reverse(BetterSelfResourceConstants.AGGREGATE)
        start_date = "2020-01-02"

        supplements = SupplementFactory.create_batch(2, user=self.user_1)
        start_time = serialize_date_to_user_localized_datetime(
            start_date, user=self.user_1
        )

        for supplement in supplements:
            SupplementLogFactory(
                user=self.user_1, supplement=supplement, time=start_time
            )

        supplement_uuids = [str(supplement.uuid) for supplement in supplements]

        kwargs = {
            "start_date": "2020-01-01",
            "end_date": "2020-01-02",
            "supplement_uuids": supplement_uuids,
        }

        response = self.client_1.post(url, data=kwargs, format="json")
        self.assertEqual(response.status_code, 200, response.data)

        self.assertIsNotNone(response.data["supplements"])

    def test_url_with_supplements_requested_filter(self):
        url = reverse(BetterSelfResourceConstants.AGGREGATE)
        start_date = "2020-01-02"

        # delete any previous data to not screw up results
        SupplementLog.objects.filter(user=self.user_1).delete()

        supplements = SupplementFactory.create_batch(2, user=self.user_1)
        start_time = serialize_date_to_user_localized_datetime(
            start_date, user=self.user_1
        )

        for supplement in supplements:
            SupplementLogFactory(
                user=self.user_1, supplement=supplement, time=start_time
            )

        # only do one uuid
        supplement_uuids = [str(supplement.uuid) for supplement in supplements[:1]]

        kwargs = {
            "start_date": "2020-01-01",
            "end_date": "2020-01-02",
            "supplement_uuids": supplement_uuids,
        }

        response = self.client_1.post(url, data=kwargs, format="json")
        self.assertEqual(response.status_code, 200, response.data)

        expected_log_count = SupplementLog.objects.filter(
            user=self.user_1, supplement__uuid__in=supplement_uuids
        ).count()

        returned_log_count = len(response.data["supplements"]["logs"])
        self.assertEqual(expected_log_count, returned_log_count)

    def test_url_with_foods_requested_filter(self):
        url = reverse(BetterSelfResourceConstants.AGGREGATE)
        start_date = "2020-01-02"
        key_type = "foods"
        key_uuid_label = "food_uuids"
        instanceFactory = FoodFactory
        instanceLogFactory = FoodLogFactory
        instanceLogModel = FoodLog

        instances = instanceFactory.create_batch(2, user=self.user_1)
        start_time = serialize_date_to_user_localized_datetime(
            start_date, user=self.user_1
        )

        for instance in instances:
            instanceLogFactory(user=self.user_1, food=instance, time=start_time)

        # only do one uuid
        instance_uuids = [str(instance.uuid) for instance in instances[:1]]

        self.assertEqual(len(instance_uuids), 1)

        kwargs = {
            "start_date": "2020-01-01",
            "end_date": "2020-01-02",
            key_uuid_label: instance_uuids,
        }

        response = self.client_1.post(url, data=kwargs, format="json")
        self.assertEqual(response.status_code, 200, response.data)

        expected_log_count = instanceLogModel.objects.filter(
            user=self.user_1, food__uuid__in=instance_uuids
        ).count()

        returned_log_count = len(response.data[key_type]["logs"])
        self.assertEqual(expected_log_count, returned_log_count)
