from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    UUIDField,
    DecimalField,
    ChoiceField,
)

from open.core.betterself.constants import INPUT_SOURCES_TUPLES, WEB_INPUT_SOURCE
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_log import SupplementLog
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.supplement_serializers import (
    SimpleSupplementReadSerializer,
)
from open.core.betterself.serializers.validators import validate_model_uuid
from open.utilities.date_and_time import get_utc_now


class SupplementLogReadSerializer(BaseModelReadSerializer):
    supplement = SimpleSupplementReadSerializer()

    class Meta:
        model = SupplementLog
        fields = (
            "display_name",
            "uuid",
            "notes",
            # "created",
            # "modified",
            "supplement",
            "source",
            "quantity",
            "time",
            "display_name",
            "duration_minutes",
        )

    def get_display_name(self, instance):
        # a janky way to always serialize a display name that sort of explains the instance
        time_ago = (get_utc_now() - instance.time).total_seconds()
        hours_ago = time_ago / 3600

        if hours_ago > 48:
            days_ago = hours_ago / 24
            relative_period_label = f"{days_ago:.01f} days ago"
        else:
            relative_period_label = f"{hours_ago:.01f} hours ago"

        name = f"{instance.quantity:.0f} x {instance.supplement.name} from {relative_period_label}"
        return name


class SupplementLogCreateUpdateSerializer(BaseCreateUpdateSerializer):
    supplement_uuid = UUIDField(source="supplement.uuid")
    # user = HiddenField(default=CurrentUserDefault())
    # uuid = UUIDField(required=False, read_only=True)
    # notes = CharField(
    #     default="",
    #     trim_whitespace=True,
    #     required=False,
    #     allow_blank=True,
    # )
    quantity = DecimalField(decimal_places=4, max_digits=10, default=1)
    source = ChoiceField(INPUT_SOURCES_TUPLES, default=WEB_INPUT_SOURCE)

    class Meta:
        model = SupplementLog
        fields = (
            "user",
            "uuid",
            "notes",
            "supplement_uuid",
            "source",
            "quantity",
            "time",
            "duration_minutes",
        )

    def validate_supplement_uuid(self, value):
        user = self.context["request"].user
        try:
            validate_model_uuid(uuid=value, model=Supplement, user=user)
        except ValidationError:
            # if it's an edit, don't allow someone to edit a log to a stack
            if self.instance:
                raise

            # we allow for supplement_stack_uuid to also be passed in here, a bit of a hack
            validate_model_uuid(uuid=value, model=SupplementStack, user=user)

        return value

    def validate(self, validated_data):
        """
        This code isn't pretty, but it's because i'm jamming supplement stack and supplements in one view
        """
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if validated_data.get("supplement"):
            supplement = validated_data.pop("supplement")
            supplement_uuid = supplement["uuid"]

            try:
                supplement = Supplement.objects.get(uuid=supplement_uuid, user=user)
                validated_data["supplement"] = supplement

            except ObjectDoesNotExist:
                # don't allow supplement stacks if it's not a create operation
                if not is_creating_instance:
                    raise

                # if it doesn't exist, it's a supplement stack
                stack = SupplementStack.objects.get(uuid=supplement_uuid, user=user)
                validated_data["stack"] = stack

        if is_creating_instance and validated_data.get("supplement"):
            if self.Meta.model.objects.filter(
                user=user,
                supplement=supplement,
                time=validated_data["time"],
            ).exists():
                raise ValidationError(
                    "Fields user, supplement, and time are not unique!"
                )
        elif is_creating_instance and validated_data.get("stack"):
            stack = validated_data["stack"]
            stack_supplements = [item.supplement for item in stack.compositions.all()]

            for supplement in stack_supplements:
                if self.Meta.model.objects.filter(
                    user=user,
                    supplement=supplement,
                    time=validated_data["time"],
                ).exists():
                    raise ValidationError(
                        "Fields user, supplement, and time are not unique!"
                    )

        return validated_data

    def create(self, validated_data):
        if validated_data.get("supplement"):
            # normal drf serializers, change nothing
            return super().create(validated_data)

        elif validated_data.get("stack"):
            stack = validated_data.pop("stack")
            stack_compositions = stack.compositions.all()

            created_instances = []
            for composition in stack_compositions:
                results = validated_data.copy()
                supplement = composition.supplement

                # a stack might have a quantity of 2 of something
                updated_quantity = results["quantity"] * composition.quantity

                results["supplement"] = supplement
                results["quantity"] = updated_quantity

                created_instance = self.Meta.model.objects.create(**results)
                created_instances.append(created_instance)

            return created_instances
