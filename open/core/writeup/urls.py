from django.urls import path

from open.core.writeup.views import GeneratedSentenceView, writeup_index, writeup_room
from open.core.writeup.constants import WriteUpResourceEndpoints

urlpatterns = [
    path(
        f"{WriteUpResourceEndpoints.GENERATED_SENTENCE}/",
        view=GeneratedSentenceView.as_view(),
        name=WriteUpResourceEndpoints.GENERATED_SENTENCE,
    ),
    path(r"", writeup_index, name="index"),
    path(r"chat/<slug:room_name>/", writeup_room, name="room"),
]
