from django.urls import path

from open.core.writeup.views import (
    writeup_index,
    writeup_room,
    GPT2MediumPromptTestView,
    WriteUpSharedPromptView,
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
        r"shared/prompts/",
        WriteUpSharedPromptView.as_view(),
        name=WriteUpResourceEndpoints.SHARED_PROMPT_NAME,
    ),
    path(
        # api.writeup.ai/shared/prompts/:uuid
        r"shared/prompts/<uuid:uuid>/",
        WriteUpSharedPromptView.as_view(),
        name=WriteUpResourceEndpoints.SHARED_PROMPT_NAME,
    ),
]
