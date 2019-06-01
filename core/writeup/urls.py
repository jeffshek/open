from django.urls import path

from core.views import GeneratedSentenceView
from core.writeup.constants import WriteUpResourceEndpoints

urlpatterns = [
    path(f"{WriteUpResourceEndpoints.GENERATED_SENTENCE}/", view=GeneratedSentenceView.as_view(),
        name=WriteUpResourceEndpoints.GENERATED_SENTENCE),
]
