from open.core.betterself.models.measurement import Measurement
from open.core.betterself.serializers.mixins import BaseModelReadSerializer


class MeasurementReadSerializer(BaseModelReadSerializer):
    class Meta:
        model = Measurement
        fields = ("uuid", "name", "short_name", "is_liquid", "display_name")
