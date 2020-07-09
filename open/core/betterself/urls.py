from django.urls import path
from open.core.betterself.constants import BetterSelfResourceConstants as RESOURCES
from open.core.betterself.views.measurement import MeasurementListView
from open.core.betterself.views.ingredients import (
    IngredientCreateListView,
    IngredientGetUpdateView,
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
]
