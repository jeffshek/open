from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.factories import (
    SupplementLogFactory,
    SupplementFactory,
    SupplementStackCompositionFactory,
    SupplementStackFactory,
    IngredientCompositionFactory,
    MeasurementFactory,
    IngredientFactory,
    ActivityLogFactory,
    ActivityFactory,
    DailyProductivityLogFactory,
    SleepLogFactory,
    WellBeingLogFactory,
    FoodFactory,
    FoodLogFactory,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_factories.py" --keepdb
"""


class TestBetterSelfFactories(TestCase):
    def test_all_betterself_factories(self):
        """
        A quick and lazy way to make sure all factories fire correctly
        """
        factories_to_test = [
            ActivityFactory,
            ActivityLogFactory,
            DailyProductivityLogFactory,
            IngredientFactory,
            IngredientCompositionFactory,
            MeasurementFactory,
            SleepLogFactory,
            SupplementFactory,
            SupplementLogFactory,
            SupplementStackFactory,
            SupplementStackCompositionFactory,
            WellBeingLogFactory,
            FoodFactory,
            FoodLogFactory,
        ]

        for factory in factories_to_test:
            created_instance = factory()
            self.assertIsNotNone(created_instance)

    def test_sleep_log_factory(self):
        # this one is so unique i need to test it separately
        sleep_logs = SleepLogFactory.create_batch(10)
        instance = sleep_logs[0]

        self.assertTrue(instance.end_time > instance.start_time)

        sleep_time = instance.end_time - instance.start_time
        sleep_time_seconds = sleep_time.seconds
        sleep_time_hours = sleep_time_seconds // 3600

        # should always range between at least 1 and 14 for test fixtures
        self.assertTrue(14 > sleep_time_hours > 1)
