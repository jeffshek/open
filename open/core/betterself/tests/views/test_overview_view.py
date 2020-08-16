from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.tests.mixins.resource_mixin import BaseTestCase

User = get_user_model()

"""
python manage.py test --pattern="*test_overview_view.py" --keepdb
"""


class OverviewTestView(BaseTestCase):
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
        kwargs = {"period": "monthly", "date": "2020-08-22"}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

        data = self.client_1.get(url).data

        expected_keys = ["period", "start_period", "end_period"]
        data_keys = data.keys()

        valid_response = set(expected_keys).issubset(data_keys)
        msg = f"Expected {expected_keys} in {data_keys}"
        self.assertTrue(valid_response, msg=msg)
