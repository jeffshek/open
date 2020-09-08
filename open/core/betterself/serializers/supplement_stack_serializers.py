from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.supplement_stack_composition_serializers import (
    SupplementStackCompositionReadSerializer,
)


class SupplementStackReadSerializer(BaseModelReadSerializer):
    compositions = SupplementStackCompositionReadSerializer(many=True)

    class Meta:
        model = SupplementStack
        fields = (
            "uuid",
            "name",
            "notes",
            "compositions",
            "display_name",
        )


class SupplementStackCreateUpdateSerializer(BaseCreateUpdateSerializer):
    class Meta:
        model = SupplementStack
        fields = (
            "uuid",
            "name",
            "user",
            "notes",
        )
