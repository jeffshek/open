from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateField, ChoiceField, CharField

from open.core.betterself.constants import (
    BETTERSELF_LOG_INPUT_SOURCES,
    WEB_INPUT_SOURCE,
)
from open.core.betterself.models.daily_productivity_log import DailyProductivityLog
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.validators import ModelValidatorsMixin
from open.utilities.date_and_time import (
    format_datetime_to_human_readable,
    yyyy_mm_dd_format_1,
)


class DailyProductivityLogReadSerializer(BaseModelReadSerializer):
    class Meta:
        model = DailyProductivityLog
        fields = (
            "uuid",
            "source",
            "date",
            "very_productive_time_minutes",
            "productive_time_minutes",
            "neutral_time_minutes",
            "distracting_time_minutes",
            "very_distracting_time_minutes",
            "notes",
            "mistakes",
            "created",
            "modified",
            "display_name",
            "pomodoro_count",
        )

    def get_display_name(self, instance):
        model = self.Meta.model
        model_name = model._meta.verbose_name

        time_label = instance.date
        serialized_time = format_datetime_to_human_readable(
            time_label, yyyy_mm_dd_format_1
        )

        display_name = f"{model_name} | Date: {serialized_time}"
        return display_name


class DailyProductivityLogCreateUpdateSerializer(
    BaseCreateUpdateSerializer, ModelValidatorsMixin
):
    # allow an regular isoformat of milliseconds also be passed
    date = DateField(input_formats=["iso-8601"])
    source = ChoiceField(choices=BETTERSELF_LOG_INPUT_SOURCES, default=WEB_INPUT_SOURCE)
    mistakes = CharField(trim_whitespace=True, default="", allow_blank=True)

    class Meta:
        model = DailyProductivityLog
        fields = (
            "source",
            "date",
            "very_productive_time_minutes",
            "productive_time_minutes",
            "neutral_time_minutes",
            "distracting_time_minutes",
            "very_distracting_time_minutes",
            "pomodoro_count",
            "notes",
            "mistakes",
            "user",
        )

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user, date=validated_data["date"],
            ).exists():
                raise ValidationError(f"Fields user and date need to be unique!")

        return validated_data
