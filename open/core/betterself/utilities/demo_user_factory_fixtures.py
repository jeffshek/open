import logging

from dateutil import relativedelta

from open.core.betterself.factories import (
    ActivityFactory,
    ActivityLogFactory,
    DailyProductivityLogFactory,
    SupplementFactory,
    SupplementLogFactory,
    WellBeingLogFactory,
    SleepLogFactory,
    FoodFactory,
    FoodLogFactory,
)
from open.core.betterself.models.activity import Activity
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.models.food import Food
from open.core.betterself.models.food_logs import FoodLog
from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.core.betterself.models.well_being_log import WellBeingLog
from open.utilities.date_and_time import get_utc_now, get_time_relative_units_ago

logger = logging.getLogger(__name__)


def create_demo_fixtures_for_user(user):
    username = user.username
    if "demo" not in username:
        raise ValueError(
            f"Cannot Run Demo Fixtures for Username without DEMO {username}"
        )

    # wipe out all the previous models and start from scratch
    models_to_clean = [
        Activity,
        ActivityLog,
        DailyProductivityLog,
        Ingredient,
        IngredientComposition,
        SleepLog,
        Supplement,
        SupplementLog,
        SupplementStack,
        SupplementStackComposition,
        WellBeingLog,
        FoodLog,
        Food,
    ]

    for model in models_to_clean:
        model.objects.filter(user=user).delete()

    # easier to see any row updates
    daily_logs_to_create = 30
    nested_models_logs_to_create = 10
    supplements_to_create = 15
    sleep_logs_to_create = 90

    activities_to_create = 40
    activities = ActivityFactory.create_batch(activities_to_create, user=user)

    for activity in activities:
        ActivityLogFactory.create_batch(
            nested_models_logs_to_create, activity=activity, user=user
        )

    productivity_logs_to_create = 90
    DailyProductivityLogFactory.create_batch(productivity_logs_to_create, user=user)

    supplements = SupplementFactory.create_batch(supplements_to_create, user=user)
    for supplement in supplements:
        SupplementLogFactory.create_batch(
            nested_models_logs_to_create, user=user, supplement=supplement
        )

    # ingredients = IngredientFactory.create_batch(fixtures_to_create, user=user)
    #
    # for ingredient in ingredients:
    #     ingredient_composition = IngredientCompositionFactory(
    #         ingredient=ingredient, user=user
    #     )
    #     supplement = SupplementFactory.create(
    #         user=user,
    #         name=ingredient.name,
    #         ingredient_compositions=[ingredient_composition],
    #     )
    #     SupplementLogFactory.create_batch(
    #         nested_models_logs_to_create, user=user, supplement=supplement
    #     )

    WellBeingLogFactory.create_batch(daily_logs_to_create, user=user)

    utc_now = get_utc_now()

    # do 2 days ago, that way you can create data faster when self-testing
    start_period = get_time_relative_units_ago(utc_now, days=2)

    sleep_dates = []
    for index in range(sleep_logs_to_create):
        sleep_date = start_period - relativedelta.relativedelta(days=index)
        sleep_dates.append(sleep_date)

    for sleep_date in sleep_dates:
        SleepLogFactory(end_time=sleep_date, user=user)

    foods = FoodFactory.create_batch(daily_logs_to_create, user=user)
    for food in foods:
        FoodLogFactory.create_batch(nested_models_logs_to_create, food=food, user=user)

    logger.info(f"Successfully Created Demo Fixtures for {user.username}")
