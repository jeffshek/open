from django.urls import path
from open.core.betterself.constants import BetterSelfResourceConstants as RESOURCES
from open.core.betterself.views.measurement import MeasurementListView
from open.core.betterself.views.ingredients_and_stuff import (
    IngredientCreateListView,
    IngredientGetUpdateView,
    IngredientCompositionCreateListView,
    IngredientCompositionGetUpdateView,
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
]
