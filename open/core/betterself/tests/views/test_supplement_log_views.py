from django.contrib.auth import get_user_model
from django.test import TestCase

from open.core.betterself.constants import (
    BetterSelfResourceConstants,
    BetterSelfTestContants,
)
from open.core.betterself.factories import (
    SupplementLogFactory,
    SupplementFactory,
)
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
)
from open.utilities.date_and_time import get_utc_now

User = get_user_model()

"""
python manage.py test --pattern="*test_supplement_log_views.py" --keepdb
dpy test open.core.betterself.tests.views.test_supplement_log_views.TestSupplementLogViews --keepdb
"""


class TestSupplementLogViews(BetterSelfResourceViewTestCaseMixin, TestCase):
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

    def test_create_view_with_bad_supplement(self):
        time = get_utc_now()

        post_data = {
            "supplement_uuid": BetterSelfTestContants.INVALID_UUID,
            "time": time.isoformat(),
            "quantity": 5,
        }

        response = self.client_1.post(self.url, data=post_data)
        self.assertEqual(response.status_code, 400, response.data)
