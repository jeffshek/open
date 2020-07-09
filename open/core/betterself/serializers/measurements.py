from rest_framework.serializers import ModelSerializer

from open.core.betterself.models.measurement import Measurement


class MeasurementReadSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "uuid",
            "name",
            "short_name",
            "is_liquid",
        )
