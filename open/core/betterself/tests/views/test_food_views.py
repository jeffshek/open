from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import BetterSelfResourceConstants
from open.core.betterself.factories import FoodFactory
from open.core.betterself.models.food import Food
from open.core.betterself.tests.mixins.resource_mixin import (
    BetterSelfResourceViewTestCaseMixin,
    GetTestsMixin,
    DeleteTestsMixin,
)

User = get_user_model()

"""
python manage.py test --pattern="*test_food_views.py" --keepdb
"""


class FoodTestView(BetterSelfResourceViewTestCaseMixin, TestCase):
    url_name = BetterSelfResourceConstants.FOODS
    model_class_factory = FoodFactory
    model_class = Food


class FoodTestGetUpdateView(
    BetterSelfResourceViewTestCaseMixin, GetTestsMixin, DeleteTestsMixin, TestCase
):
    url_name = BetterSelfResourceConstants.FOODS
    model_class_factory = FoodFactory
    model_class = Food
