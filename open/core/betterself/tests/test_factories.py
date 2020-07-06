from django.contrib.auth import get_user_model
from django.test import TestCase

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
            IngredientFactory,
            MeasurementFactory,
            IngredientCompositionFactory,
            SupplementFactory,
            SupplementStackFactory,
            SupplementStackCompositionFactory,
            SupplementLogFactory,
            DailyProductivityLogFactory,
            ActivityFactory,
            ActivityLogFactory,
        ]

        for factory in factories_to_test:
            created_instance = factory()
            self.assertIsNotNone(created_instance)

    def test_supplement_factory(self):
        expected_name = "test"
        supplement = SupplementFactory(name=expected_name)
        self.assertEqual(supplement.name, expected_name)

    def test_supplement_log_factory(self):
        quantity = 50
        supplement_log = SupplementLogFactory(quantity=quantity)
        self.assertEqual(supplement_log.quantity, quantity)
