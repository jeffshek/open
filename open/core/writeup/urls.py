from django.urls import path

from open.core.writeup.constants import WriteUpResourceEndpoints
from open.core.writeup.views import GPT2MediumPromptTestView, WriteUpPromptView

urlpatterns = [
    path(
        f"{WriteUpResourceEndpoints.GENERATED_SENTENCE}/",
        view=GPT2MediumPromptTestView.as_view(),
        name=WriteUpResourceEndpoints.GENERATED_SENTENCE,
    ),
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
