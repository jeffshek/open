from django.core.exceptions import ValidationError
from rest_framework.fields import UUIDField, SerializerMethodField

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.serializers.ingredient_serializers import (
    IngredientReadSerializer,
)
from open.core.betterself.serializers.measurement_serializers import (
    MeasurementReadSerializer,
)
from open.core.betterself.serializers.mixins import (
    BaseCreateUpdateSerializer,
    BaseModelReadSerializer,
)
from open.core.betterself.serializers.validators import validate_model_uuid


class IngredientCompositionReadSerializer(BaseModelReadSerializer):
    ingredient = IngredientReadSerializer()
    measurement = MeasurementReadSerializer()
    display_name = SerializerMethodField()

    class Meta:
        model = IngredientComposition
        fields = (
            "uuid",
            "ingredient",
            "measurement",
            "quantity",
            "notes",
            "display_name",
            "created",
            "modified",
        )

    def get_display_name(self, instance):
        name = f"{instance.ingredient.name} {instance.quantity:.2f}{instance.measurement.short_name}"
        return name


class IngredientCompositionCreateUpdateSerializer(BaseCreateUpdateSerializer):
    ingredient_uuid = UUIDField(source="ingredient.uuid")
    measurement_uuid = UUIDField(source="measurement.uuid")

    class Meta:
        model = IngredientComposition
        fields = (
            "uuid",
            "ingredient_uuid",
            "measurement_uuid",
            "quantity",
            "user",
            "notes",
        )

    def validate_ingredient_uuid(self, value):
        user = self.context["request"].user
        validate_model_uuid(uuid=value, model=Ingredient, user=user)
        return value

    def validate_measurement_uuid(self, value):
        validate_model_uuid(uuid=value, model=Measurement)
        return value

    def validate(self, validated_data):
        user = self.context["request"].user
        is_creating_instance = not self.instance

        if validated_data.get("ingredient"):
            ingredient_uuid = validated_data.pop("ingredient")["uuid"]
            ingredient = Ingredient.objects.get(uuid=ingredient_uuid, user=user)
            validated_data["ingredient"] = ingredient

        if validated_data.get("measurement"):
            measurement_uuid = validated_data.pop("measurement")["uuid"]
            measurement = Measurement.objects.get(uuid=measurement_uuid)
            validated_data["measurement"] = measurement

        # check for uniqueconstraints issues with creation
        # for updates, probably be a little bit easier
        # and skip for now
        if is_creating_instance:
            if self.Meta.model.objects.filter(
                user=user,
                ingredient=ingredient,
                measurement=measurement,
                quantity=validated_data["quantity"],
            ).exists():
                raise ValidationError(
                    "Fields user, ingredient, measurement, and quantity are not unique!"
                )

        return validated_data
