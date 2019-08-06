from django.urls import path

from open.core.writeup.views import (
    writeup_index,
    writeup_room,
    GPT2MediumPromptTestView,
    WriteUpPromptView,
)
from open.core.writeup.constants import WriteUpResourceEndpoints

urlpatterns = [
    path(
        f"{WriteUpResourceEndpoints.GENERATED_SENTENCE}/",
        view=GPT2MediumPromptTestView.as_view(),
        name=WriteUpResourceEndpoints.GENERATED_SENTENCE,
    ),
    path(r"", writeup_index, name="index"),
    path(r"chat/<slug:room_name>/", writeup_room, name="room"),
    path(
        r"prompts/", WriteUpPromptView.as_view(), name=WriteUpResourceEndpoints.PROMPTS
    ),
    path(
        # api.writeup.ai/prompts/:uuid
        r"prompts/<uuid:uuid>/",
        WriteUpPromptView.as_view(),
        name=WriteUpResourceEndpoints.PROMPTS,
    ),
]
