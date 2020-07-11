from django.urls import path
from open.core.betterself.constants import BetterSelfResourceConstants as RESOURCES
from open.core.betterself.views.activity_views import (
    ActivityGetUpdateView,
    ActivityCreateListView,
)
from open.core.betterself.views.measurement import MeasurementListView
from open.core.betterself.views.ingredient_views import (
    IngredientCreateListView,
    IngredientGetUpdateView,
)
from open.core.betterself.views.ingredient_composition_views import (
    IngredientCompositionCreateListView,
    IngredientCompositionGetUpdateView,
)
from open.core.betterself.views.supplement_log_views import (
    SupplementLogCreateListView,
    SupplementLogGetUpdateView,
)
from open.core.betterself.views.supplement_views import (
    SupplementCreateListView,
    SupplementGetUpdateView,
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
]
