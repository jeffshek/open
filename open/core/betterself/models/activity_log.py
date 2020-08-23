from django.db.models import (
    CharField,
    ForeignKey,
    IntegerField,
    DateTimeField,
    CASCADE,
)

from open.core.betterself.constants import (
    INPUT_SOURCES_TUPLES,
    WEB_INPUT_SOURCE,
    BetterSelfResourceConstants,
)
from open.core.betterself.models.activity import Activity
from open.utilities.models import BaseModelWithUserGeneratedContent


class ActivityLog(BaseModelWithUserGeneratedContent):
    """
    Represents any particular type of event a user may have done
        - ie. Meditation, running, take dog the park, etc.

    This doesn't really get to the crux of how do you record a state of mind that's
    frustrating like depression/flu (both of which share oddly similar mental states),
    which if this is one thing BetterSelf cures for you, then it's a success.

    I just haven't figured the most appropriate way to model / store such information.
    """

    RESOURCE_NAME = BetterSelfResourceConstants.ACTIVITY_LOGS

    activity = ForeignKey(Activity, on_delete=CASCADE)
    source = CharField(
        max_length=50, choices=INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE
    )
    duration_minutes = IntegerField(blank=True, null=True)
    time = DateTimeField()

    class Meta:
        unique_together = (("time", "user", "activity"),)
        # ordering = ["user", "-time"]
        ordering = ["-time"]
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return "{} {}".format(self.activity, self.time)
