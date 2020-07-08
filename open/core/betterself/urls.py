from django.urls import path
from open.core.betterself.constants import BetterSelfResourceConstants as RESOURCES
from open.core.betterself.views import MeasurementListView, IngredientListView

urlpatterns = [
    path(
        f"{RESOURCES.MEASUREMENTS}/",
        view=MeasurementListView.as_view(),
        name=RESOURCES.MEASUREMENTS,
    ),
    path(
        f"{RESOURCES.INGREDIENTS}/",
        view=IngredientListView.as_view(),
        name=RESOURCES.INGREDIENTS,
    ),
]
