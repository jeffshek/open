import logging

from open.core.betterself.factories import (
    ActivityFactory,
    ActivityLogFactory,
    DailyProductivityLogFactory,
    IngredientFactory,
    SupplementFactory,
    SupplementLogFactory,
    WellBeingLogFactory,
    SleepLogFactory,
)
from open.core.betterself.models.activity import Activity
from open.core.betterself.models.activity_log import ActivityLog
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.ingredient_composition import IngredientComposition

# from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.core.betterself.models.well_being_log import WellBeingLog

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
    ]

    for model in models_to_clean:
        model.objects.filter(user=user).delete()

    fixture_to_create = 5
    daily_logs_to_create = 50
    activities = ActivityFactory.create_batch(fixture_to_create, user=user)
    for activity in activities:
        ActivityLogFactory.create_batch(fixture_to_create, activity=activity, user=user)

    DailyProductivityLogFactory.create_batch(daily_logs_to_create, user=user)
    ingredients = IngredientFactory.create_batch(fixture_to_create, user=user)

    for ingredient in ingredients:
        supplement = SupplementFactory.create(user=user, name=ingredient.name)
        SupplementLogFactory.create_batch(
            fixture_to_create, user=user, supplement=supplement
        )

    WellBeingLogFactory.create_batch(daily_logs_to_create, user=user)
    SleepLogFactory.create_batch(daily_logs_to_create, user=user)

    logger.info(f"Successfully Created Demo Fixtures for {user.username}")
