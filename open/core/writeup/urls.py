from django.urls import path

from open.core.writeup.constants import WriteUpResourceEndpoints
from open.core.writeup.views import (
    GPT2MediumPromptDebugView,
    WriteUpPromptView,
    WriteUpPromptVoteView,
    WriteUpFlaggedPromptView,
    WriteUpPromptListCreateView,
)

urlpatterns = [
    path(
        f"{WriteUpResourceEndpoints.GENERATED_SENTENCE}/",
        view=GPT2MediumPromptDebugView.as_view(),
        name=WriteUpResourceEndpoints.GENERATED_SENTENCE,
    ),
    path(
        r"prompts/",
        WriteUpPromptListCreateView.as_view(),
        name=WriteUpResourceEndpoints.PROMPTS,
    ),
    path(
        # frontend urls are like
        # writeup.ai/prompts/:uuid/
        r"prompts/<uuid:prompt_uuid>/",
        WriteUpPromptView.as_view(),
        name=WriteUpResourceEndpoints.PROMPTS,
    ),
    path(
        r"prompts/<uuid:prompt_uuid>/votes/",
        WriteUpPromptVoteView.as_view(),
        name=WriteUpResourceEndpoints.PROMPT_VOTES,
    ),
    path(
        r"prompts/<uuid:prompt_uuid>/flags/",
        WriteUpFlaggedPromptView.as_view(),
        name=WriteUpResourceEndpoints.PROMPT_FLAGS,
    ),
]
