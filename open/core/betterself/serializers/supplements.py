from rest_framework.serializers import ModelSerializer

from open.core.betterself.models.supplement import Supplement


class SupplementReadSerializer(ModelSerializer):
    class Meta:
        model = Supplement
        fields = (
            "uuid",
            "notes",
            "name",
        )
