from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import MeasurementFactory
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_measurement_views.py" --keepdb
"""


class TestMeasurementView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.MEASUREMENTS
    model_class_factory = MeasurementFactory
    model_class = Measurement

    def test_view(self):
        data = self.client_1.get(self.url).data
        self.assertEqual(len(data), 5)

    def test_no_access_view(self):
        """
        Doesn't apply here, measurements are available for all.
        """
        return
