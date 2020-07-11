from django.contrib.auth import get_user_model
from django.test import TestCase

from open.core.betterself.constants import (
    BetterSelfResourceConstants,
    BetterSelfTestContants,
)
from open.core.betterself.factories import ActivityFactory, ActivityLogFactory
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
)
from open.utilities.date_and_time import get_utc_now

User = get_user_model()

"""
python manage.py test --pattern="*test_activity_log_views.py" --keepdb
"""


class ActivityLogView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.ACTIVITY_LOGS
    model_class_factory = ActivityLogFactory
    model_class = ActivityLog

    def test_create_view(self):
        activity = ActivityFactory(name=BetterSelfTestContants.NAME_1, user=self.user_1)
        current_time = get_utc_now()

        post_data = {
            "activity_uuid": str(activity.uuid),
            "time": current_time.isoformat(),
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 200, response.data)

        data = response.data
        value_name = data["activity"]["name"]
        self.assertEqual(BetterSelfTestContants.NAME_1, value_name)
