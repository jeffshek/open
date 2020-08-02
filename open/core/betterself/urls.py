from django.urls import path

from open.core.betterself.constants import BetterSelfResourceConstants as RESOURCES
from open.core.betterself.views.activity_log_views import (
    ActivityLogCreateListView,
    ActivityLogGetUpdateView,
)
from open.core.betterself.views.activity_views import (
    ActivityGetUpdateView,
    ActivityCreateListView,
)
from open.core.betterself.views.daily_productivity_log_views import (
    DailyProductivityLogCreateListView,
    DailyProductivityLogGetUpdateView,
)
from open.core.betterself.views.food_log_views import (
    FoodLogGetUpdateView,
    FoodLogCreateListView,
)
from open.core.betterself.views.food_views import FoodGetUpdateView, FoodCreateListView
from open.core.betterself.views.ingredient_composition_views import (
    IngredientCompositionCreateListView,
    IngredientCompositionGetUpdateView,
)
from open.core.betterself.views.ingredient_views import (
    IngredientCreateListView,
    IngredientGetUpdateView,
)
from open.core.betterself.views.measurement import MeasurementListView
from open.core.betterself.views.sleep_log_views import (
    SleepLogCreateListView,
    SleepLogGetUpdateView,
)
from open.core.betterself.views.supplement_log_views import (
    SupplementLogCreateListView,
    SupplementLogGetUpdateView,
)
from open.core.betterself.views.supplement_views import (
    SupplementCreateListView,
    SupplementGetUpdateView,
)
from open.core.betterself.views.well_being_log_views import (
    WellBeingLogGetUpdateView,
    WellBeingLogCreateListView,
)

urlpatterns = [
    path(
        f"{RESOURCES.MEASUREMENTS}/",
        view=MeasurementListView.as_view(),
        name=RESOURCES.MEASUREMENTS,
    ),
    path(
        f"{RESOURCES.INGREDIENTS}/",
        view=IngredientCreateListView.as_view(),
        name=RESOURCES.INGREDIENTS,
    ),
    path(
        f"{RESOURCES.INGREDIENTS}/<uuid:uuid>/",
        view=IngredientGetUpdateView.as_view(),
        name=RESOURCES.INGREDIENTS,
    ),
    path(
        f"{RESOURCES.INGREDIENT_COMPOSITIONS}/",
        view=IngredientCompositionCreateListView.as_view(),
        name=RESOURCES.INGREDIENT_COMPOSITIONS,
    ),
    path(
        f"{RESOURCES.INGREDIENT_COMPOSITIONS}/<uuid:uuid>/",
        view=IngredientCompositionGetUpdateView.as_view(),
        name=RESOURCES.INGREDIENT_COMPOSITIONS,
    ),
    path(
        f"{RESOURCES.SUPPLEMENTS}/",
        view=SupplementCreateListView.as_view(),
        name=RESOURCES.SUPPLEMENTS,
    ),
    path(
        f"{RESOURCES.SUPPLEMENTS}/<uuid:uuid>/",
        view=SupplementGetUpdateView.as_view(),
        name=RESOURCES.SUPPLEMENTS,
    ),
    path(
        f"{RESOURCES.SUPPLEMENT_LOGS}/",
        view=SupplementLogCreateListView.as_view(),
        name=RESOURCES.SUPPLEMENT_LOGS,
    ),
    path(
        f"{RESOURCES.SUPPLEMENT_LOGS}/<uuid:uuid>/",
        view=SupplementLogGetUpdateView.as_view(),
        name=RESOURCES.SUPPLEMENT_LOGS,
    ),
    path(
        f"{RESOURCES.ACTIVITIES}/",
        view=ActivityCreateListView.as_view(),
        name=RESOURCES.ACTIVITIES,
    ),
    path(
        f"{RESOURCES.ACTIVITIES}/<uuid:uuid>/",
        view=ActivityGetUpdateView.as_view(),
        name=RESOURCES.ACTIVITIES,
    ),
    path(
        f"{RESOURCES.ACTIVITY_LOGS}/",
        view=ActivityLogCreateListView.as_view(),
        name=RESOURCES.ACTIVITY_LOGS,
    ),
    path(
        f"{RESOURCES.ACTIVITY_LOGS}/<uuid:uuid>/",
        view=ActivityLogGetUpdateView.as_view(),
        name=RESOURCES.ACTIVITY_LOGS,
    ),
    path(
        f"{RESOURCES.DAILY_PRODUCTIVITY_LOGS}/",
        view=DailyProductivityLogCreateListView.as_view(),
        name=RESOURCES.DAILY_PRODUCTIVITY_LOGS,
    ),
    path(
        f"{RESOURCES.DAILY_PRODUCTIVITY_LOGS}/<uuid:uuid>/",
        view=DailyProductivityLogGetUpdateView.as_view(),
        name=RESOURCES.DAILY_PRODUCTIVITY_LOGS,
    ),
    path(
        f"{RESOURCES.WELL_BEING_LOGS}/",
        view=WellBeingLogCreateListView.as_view(),
        name=RESOURCES.WELL_BEING_LOGS,
    ),
    path(
        f"{RESOURCES.WELL_BEING_LOGS}/<uuid:uuid>/",
        view=WellBeingLogGetUpdateView.as_view(),
        name=RESOURCES.WELL_BEING_LOGS,
    ),
    path(
        f"{RESOURCES.SLEEP_LOGS}/",
        view=SleepLogCreateListView.as_view(),
        name=RESOURCES.SLEEP_LOGS,
    ),
    path(
        f"{RESOURCES.SLEEP_LOGS}/<uuid:uuid>/",
        view=SleepLogGetUpdateView.as_view(),
        name=RESOURCES.SLEEP_LOGS,
    ),
    path(
        f"{RESOURCES.FOODS}/", view=FoodCreateListView.as_view(), name=RESOURCES.FOODS,
    ),
    path(
        f"{RESOURCES.FOODS}/<uuid:uuid>/",
        view=FoodGetUpdateView.as_view(),
        name=RESOURCES.FOODS,
    ),
    path(
        f"{RESOURCES.FOOD_LOGS}/",
        view=FoodLogCreateListView.as_view(),
        name=RESOURCES.FOOD_LOGS,
    ),
    path(
        f"{RESOURCES.FOOD_LOGS}/<uuid:uuid>/",
        view=FoodLogGetUpdateView.as_view(),
        name=RESOURCES.FOOD_LOGS,
    ),
]
