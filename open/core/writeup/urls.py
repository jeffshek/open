from django.urls import path

from open.core.writeup.views import GeneratedSentenceView
from open.core.writeup.constants import WriteUpResourceEndpoints

urlpatterns = [
    path(
        f"{WriteUpResourceEndpoints.GENERATED_SENTENCE}/",
        view=GeneratedSentenceView.as_view(),
        name=WriteUpResourceEndpoints.GENERATED_SENTENCE,
    )
]
