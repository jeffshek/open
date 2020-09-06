from open.core.betterself.models.supplement_stack import SupplementStack
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)


class SupplementStackReadSerializer(BaseModelReadSerializer):
    class Meta:
        model = SupplementStack
        fields = (
            "uuid",
            "name",
            "notes",
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
