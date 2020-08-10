from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import FoodLogFactory
from open.core.betterself.models.food_logs import FoodLog
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_food_log_views.py" --keepdb
"""


class FoodLogTestView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.FOODS
    model_class_factory = FoodLogFactory
    model_class = FoodLog


class FoodLogTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.FOODS
    model_class_factory = FoodLogFactory
    model_class = FoodLog
