from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField

from open.core.betterself.constants import INPUT_SOURCES_TUPLES, WEB_INPUT_SOURCE
from open.core.betterself.models.sleep_log import SleepLog
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.validators import ModelValidatorsMixin
from open.utilities.date_and_time import format_datetime_to_human_readable


class SleepLogReadSerializer(BaseModelReadSerializer):
    class Meta:
        model = SleepLog
        fields = (
            "source",
            "start_time",
            "end_time",
            "notes",
            # "created",
            # "modified",
            "uuid",
            "display_name",
            "duration_minutes",
            "duration_hours",
        )

    def get_display_name(self, instance):
        model = self.Meta.model
        model_name = model._meta.verbose_name

        start_time = instance.start_time
        start_time_serialized = format_datetime_to_human_readable(start_time)

        duration_minutes = instance.duration_minutes

        display_name = f"{model_name} | Start Time: {start_time_serialized} UTC. Duration {duration_minutes:.0f} minutes."
        return display_name


class SleepLogCreateUpdateSerializer(BaseCreateUpdateSerializer, ModelValidatorsMixin):
    source = ChoiceField(INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)

    class Meta:
        model = SleepLog
        fields = (
            "source",
            "start_time",
            "end_time",
            "notes",
            "user",
        )

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        end_time = validated_data.get("end_time") or self.instance.end_time
        start_time = validated_data.get("start_time") or self.instance.start_time

        if start_time > end_time:
            raise ValidationError("End Time Must Occur After Start")

        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user,
                start_time=validated_data["start_time"],
                end_time=validated_data["end_time"],
            ).exists():
                raise ValidationError(
                    f"Fields user, start_time, and end_time are not unique!"
                )

            queryset = SleepLog.objects.filter(
                user=user, end_time__gte=start_time, start_time__lte=end_time
            )

            if queryset.exists():
                duplicated = queryset.first()
                start_time_label = duplicated.start_time.date()

                raise ValidationError(
                    f"Sleep Periods cannot overlap! Found overlapping on {start_time_label}"
                )

        return validated_data
