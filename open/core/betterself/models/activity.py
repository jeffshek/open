from django.db.models import CharField, BooleanField

from open.core.betterself.constants import BetterSelfResourceConstants
from open.utilities.models import BaseModelWithUserGeneratedContent


class Activity(BaseModelWithUserGeneratedContent):
    """
    Users will probably put stuff like "Ate Breakfast", but ideally I want something that can
    support an Activity like "Morning Routine" would consists of multiple ActivityActions

    This is why it's set as foreign key from ActivityEvent, I don't want to overengineer and build
    the entire foreign key relationships, but I also don't want to build a crappy hole that I have to dig out of.
    """

    RESOURCE_NAME = BetterSelfResourceConstants.ACTIVITIES

    name = CharField(max_length=300)
    # Was this significant? IE. Got married? Had a Kid? (Congrats!) Had surgery? New Job? Decided to quit smoking?
    # Mark significant events that might change all future events.
    # Eventually used in charts as "markers/signals" in a chart to show
    # IE. Once you decided to quit smoking --- > This is your heart rate.
    is_significant_activity = BooleanField(default=False)
    # Is this an user_activity you hate / want to avoid?
    # Are there certain patterns (sleep, diet, supplements, other activities) that lead to negative activities?
    # IE - Limited sleep impact decision making (probably).
    # Can we figure out if there are certain things you do ahead that limit sleep?
    # Can we figure out if there are certain behaviors you can avoid so this doesn't happen?
    # Are there certain foods that will likely cause a negative user_activity?
    # Personally - Eating foods with lots of preservatives causes depression/flu like symptoms that last for 1-2 days

    # i regret naming _activity at the boolean fields ...
    is_negative_activity = BooleanField(default=False)
    # I find certain events are complete days, ie. Being sick with an impacted wisdom tooth was the worst.
    is_all_day_activity = BooleanField(default=False)

    class Meta:
        unique_together = (("name", "user"),)
        ordering = ["name"]
        verbose_name_plural = "Activities"
