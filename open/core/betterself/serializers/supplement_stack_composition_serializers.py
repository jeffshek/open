from django.core.exceptions import ValidationError
from rest_framework.fields import UUIDField, DecimalField

from open.core.betterself.models.supplement import Supplement
from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.models.supplement_stack_composition import (
    SupplementStackComposition,
)
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.simple_generic_serializer import (
    create_name_uuid_serializer,
)
from open.core.betterself.serializers.supplement_serializers import (
    SimpleSupplementReadSerializer,
)
from open.core.betterself.serializers.validators import validate_model_uuid


class SupplementStackCompositionReadSerializer(BaseModelReadSerializer):
    supplement = SimpleSupplementReadSerializer()
    stack = create_name_uuid_serializer(SupplementStack)

    class Meta:
        model = SupplementStackComposition
        fields = ("uuid", "supplement", "stack", "quantity", "display_name")


class SupplementStackCompositionCreateUpdateSerializer(BaseCreateUpdateSerializer):
    supplement_uuid = UUIDField(source="supplement.uuid")
    stack_uuid = UUIDField(source="stack.uuid")
    quantity = DecimalField(decimal_places=4, max_digits=10, default=1)

    class Meta:
        model = SupplementStackComposition
        fields = (
            "user",
            "uuid",
            "notes",
            "supplement_uuid",
            "stack_uuid",
            "quantity",
        )

    def validate_supplement_uuid(self, value):
        user = self.context["request"].user
        validate_model_uuid(uuid=value, model=Supplement, user=user)
        return value

    def validate_stack_uuid(self, value):
        user = self.context["request"].user
        validate_model_uuid(uuid=value, model=SupplementStack, user=user)
        return value

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if validated_data.get("supplement"):
            supplement_uuid = validated_data.pop("supplement")["uuid"]
            supplement = Supplement.objects.get(uuid=supplement_uuid, user=user)
            validated_data["supplement"] = supplement

        if validated_data.get("stack"):
            stack_uuid = validated_data.pop("stack")["uuid"]
            stack = SupplementStack.objects.get(uuid=stack_uuid, user=user)
            validated_data["stack"] = stack

        # check for uniqueconstraints issues with creation
        # for updates, probably be a little bit easier
        # and skip for now
        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user,
                stack=validated_data["stack"],
                supplement=validated_data["supplement"],
            ).exists():
                raise ValidationError(
                    "Fields supplement stack and supplement are not unique"
                )
        else:
            # if this is changing a supplement in a stack, make sure no conflicts with other compositions
            if validated_data.get("supplement"):
                # if updating, make sure that there are no other compositions with the same stack materials
                if (
                    self.Meta.model.objects.filter(
                        user=user,
                        stack=self.instance.stack,
                        supplement=validated_data["supplement"],
                    )
                    .exclude(uuid=self.instance.uuid)
                    .exists()
                ):
                    raise ValidationError(
                        "Fields supplement stack and supplement name are not unique. Only a unique supplement allowed per stack."
                    )

        return validated_data
