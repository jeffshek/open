from django.core.exceptions import ValidationError
from rest_framework.fields import UUIDField, HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.serializers.measurement_serializers import (
    MeasurementReadSerializer,
)
from open.core.betterself.serializers.ingredient_serializers import (
    IngredientReadSerializer,
)
from open.core.betterself.serializers.validators import validate_model_uuid


class IngredientCompositionReadSerializer(ModelSerializer):
    ingredient = IngredientReadSerializer()
    measurement = MeasurementReadSerializer()

    class Meta:
        model = IngredientComposition
        fields = ("uuid", "ingredient", "measurement", "quantity", "notes")


class IngredientCompositionCreateUpdateSerializer(ModelSerializer):
    uuid = UUIDField(required=False, read_only=True)
    user = HiddenField(default=CurrentUserDefault())
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
        validate_model_uuid(Ingredient, uuid=value, user=user)
        return value

    def validate_measurement_uuid(self, value):
        validate_model_uuid(Measurement, uuid=value)
        return value

    def validate(self, validated_data):
        user = self.context["request"].user

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
        if not self.instance:
            if self.Meta.model.objects.filter(
                user=user,
                ingredient=ingredient,
                measurement=measurement,
                quantity=validated_data["quantity"],
            ).exists():
                raise ValidationError(
                    f"Fields user, ingredient, measurement, and quantity are not unique!"
                )

        return validated_data

    def create(self, validated_data):
        create_model = self.Meta.model
        obj = create_model.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
