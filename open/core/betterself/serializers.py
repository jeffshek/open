from rest_framework.fields import UUIDField
from rest_framework.serializers import ModelSerializer

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.models.supplement import Supplement


class SupplementReadSerializer(ModelSerializer):
    class Meta:
        model = Supplement
        fields = (
            "uuid",
            "notes",
            "name",
        )


class MeasurementReadSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "uuid",
            "notes",
            "name",
            "short_name",
            "is_liquid",
        )


class IngredientReadSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes")


class IngredientCreateSerializer(ModelSerializer):
    uuid = UUIDField(required=False, read_only=True)

    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes")

    def create(self, validated_data):
        user = self.context["request"].user
        create_model = self.Meta.model
        name = validated_data.pop("name")
        obj, _ = create_model.objects.get_or_create(
            user=user, name=name, defaults=validated_data
        )
        return obj
