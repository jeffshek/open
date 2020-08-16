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
        kwargs = {"period": "monthly"}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)
        self.assertIsNotNone(url)

    def test_view(self):
        kwargs = {"period": "monthly"}
        url = reverse(BetterSelfResourceConstants.OVERVIEWS, kwargs=kwargs)

        response = self.client_1.get(url)
        self.assertEqual(response.status_code, 200, response.data)
