from django.db.models import (
    CharField,
    DateTimeField,
    PositiveSmallIntegerField,
)

from open.core.betterself.constants import (
    INPUT_SOURCES_TUPLES,
    WEB_INPUT_SOURCE,
    BetterSelfResourceConstants,
)
from open.utilities.date_and_time import get_utc_now
from open.utilities.models import BaseModelWithUserGeneratedContent


class WellBeingLog(BaseModelWithUserGeneratedContent):
    """
    Meant to capture both physical and mental well-being

    IE. Someone could be happy and tired, or sad and strong(?) less-likely

    Capture enough data to be helpful to diagnose chronic
    """

    RESOURCE_NAME = BetterSelfResourceConstants.WELL_BEING_LOGS

    time = DateTimeField(default=get_utc_now)

    # differentiate between feeling how a person may feel mentally versus physically
    # do as a score of 1-10
    mental_value = PositiveSmallIntegerField(null=True, blank=True)
    physical_value = PositiveSmallIntegerField(null=True, blank=True)

    source = CharField(
        max_length=50, choices=INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE
    )

    class Meta:
        unique_together = ("user", "time")
        ordering = ["user", "-time"]
        verbose_name = "Well Being Log"
        verbose_name_plural = "Well Being Logs"

    def __str__(self):
        return "User - {}, Mood - {} at {}".format(self.user, self.value, self.time)
