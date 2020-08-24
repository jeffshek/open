from django.core.exceptions import ValidationError
from django.db.models import CharField, DateTimeField

from open.core.betterself.constants import (
    INPUT_SOURCES_TUPLES,
    BetterSelfResourceConstants,
)
from open.utilities.date_and_time import (
    format_datetime_to_human_readable,
    convert_timedelta_to_minutes,
)
from open.utilities.models import BaseModelWithUserGeneratedContent


class SleepLog(BaseModelWithUserGeneratedContent):
    """
    Records per each time a person falls asleep that combined across 24 hours is a way to see how much sleep
    a person gets.
    """

    RESOURCE_NAME = BetterSelfResourceConstants.SLEEP_LOGS

    source = CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    start_time = DateTimeField()
    end_time = DateTimeField()

    class Meta:
        verbose_name = "Sleep Log"
        verbose_name_plural = "Sleep Logs"
        ordering = ["user", "-end_time"]

    def __str__(self):
        return f"{self.user_id} {format_datetime_to_human_readable(self.start_time)} {format_datetime_to_human_readable(self.end_time)}"

    def save(self, *args, **kwargs):
        # now thinking about this a little bit more ... not sure if this really matters. if the user puts wrong
        # information in why should one try to fix it?
        if self.end_time <= self.start_time:
            raise ValidationError("End Time must be greater than Start Time")

        # make sure that there are no overlaps for activities
        # https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
        # thinking about this a little - sort of wonder, shouldn't i just allow this to let people try out multiple devices
        # like a fitbit watch and an apple sleep?
        # queryset = SleepLog.objects.filter(
        #     user=self.user, end_time__gte=self.start_time, start_time__lte=self.end_time
        # )
        # if queryset.exists():
        #     duplicated = queryset.first()
        #
        #     raise ValidationError(
        #         f"Overlapping Periods found when saving Sleep Activity! Found {duplicated.start_time} {duplicated.end_time}"
        #     )

        super().save(*args, **kwargs)

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def duration_minutes(self):
        minutes = convert_timedelta_to_minutes(self.duration)
        return minutes

    @property
    def duration_hours(self):
        minutes = convert_timedelta_to_minutes(self.duration)
        hours = minutes / 60
        return hours
