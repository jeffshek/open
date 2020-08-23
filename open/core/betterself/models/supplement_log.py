from django.db.models import (
    ForeignKey,
    DecimalField,
    CASCADE,
    CharField,
    DateTimeField,
    PositiveIntegerField,
)

from open.core.betterself.constants import (
    WEB_INPUT_SOURCE,
    INPUT_SOURCES_TUPLES,
    BetterSelfResourceConstants,
)
from open.core.betterself.models.supplement import Supplement
from open.utilities.models import BaseModelWithUserGeneratedContent


class SupplementLog(BaseModelWithUserGeneratedContent):
    RESOURCE_NAME = BetterSelfResourceConstants.SUPPLEMENT_LOGS

    supplement = ForeignKey(Supplement, on_delete=CASCADE)
    source = CharField(
        max_length=50, choices=INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE
    )
    quantity = DecimalField(max_digits=10, decimal_places=2)
    # what time did the user take the five hour energy? use the time model
    # so eventually (maybe never) can do half-life analysis
    time = DateTimeField()
    duration_minutes = PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "time", "supplement")
        # ordering = ["user", "-time"]
        ordering = ["-time"]
        verbose_name = "Supplement Log"
        verbose_name_plural = "Supplement Logs"

    def __str__(self):
        formatted_time = self.time.strftime("%Y-%m-%d %I:%M%p")
        return f"{self.quantity:.0f} {self.supplement.name} {formatted_time} from {self.source} event"
