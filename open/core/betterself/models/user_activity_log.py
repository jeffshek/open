from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    IntegerField,
    DateTimeField,
)

from open.core.betterself.constants import INPUT_SOURCES_TUPLES, WEB_INPUT_SOURCE
from open.core.betterself.models.user_activity import UserActivity
from open.utilities.models import BaseModelWithUserGeneratedContent


class UserActivityLog(BaseModelWithUserGeneratedContent):
    """
    Represents any particular type of event a user may have done
        - ie. Meditation, running, take dog the park, etc.

    This doesn't really get to the crux of how do you record a state of mind that's
    frustrating like depression/flu (both of which share oddly similar mental states),
    which if this is one thing BetterSelf cures for you, then it's a success.

    I just haven't figured the most appropriate way to model / store such information.
    """

    user_activity = ForeignKey(UserActivity)
    source = CharField(
        max_length=50, choices=INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE
    )
    duration_minutes = IntegerField(default=0)
    time = DateTimeField()
    notes = TextField(default="")

    class Meta:
        unique_together = (("time", "user", "user_activity"),)
        ordering = ["user", "-time"]

    def __str__(self):
        return "{} {}".format(self.user_activity, self.time)
