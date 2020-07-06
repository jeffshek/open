from django.core.exceptions import ValidationError
from django.db.models import CharField, TextField, DateTimeField

from open.core.betterself.constants import INPUT_SOURCES_TUPLES
from open.utilities.models import BaseModelWithUserGeneratedContent


class SleepLog(BaseModelWithUserGeneratedContent):
    """
    Records per each time a person falls asleep that combined across 24 hours is a way to see how much sleep
    a person gets.
    """

    source = CharField(max_length=50, choices=INPUT_SOURCES_TUPLES)
    start_time = DateTimeField()
    end_time = DateTimeField()
    notes = TextField(default="")

    class Meta:
        verbose_name = "Sleep Activity Log"
        verbose_name_plural = "Sleep Activity Logs"
        ordering = ["user", "-end_time"]

    def __str__(self):
        return "{obj.user} {obj.start_time} {obj.end_time}".format(obj=self)

    def save(self, *args, **kwargs):
        if self.end_time <= self.start_time:
            raise ValidationError("End Time must be greater than Start Time")

        # make sure that there are no overlaps for activities
        # https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
        queryset = SleepLog.objects.filter(
            user=self.user, end_time__gte=self.start_time, start_time__lte=self.end_time
        )

        # sometimes save just happens for an update, exclude so wont always fail
        if self.pk:
            queryset = queryset.exclude(id=self.pk)

        if queryset.exists():
            raise ValidationError(
                "Overlapping Periods found when saving Sleep Activity. Found {}".format(
                    queryset
                )
            )

        super().save(*args, **kwargs)

    @property
    def duration(self):
        return self.end_time - self.start_time
