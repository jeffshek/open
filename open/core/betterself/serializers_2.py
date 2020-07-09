from django.core.exceptions import ValidationError
from rest_framework.fields import UUIDField, HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from open.core.betterself.models.ingredient import Ingredient
from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.measurement import Measurement
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.utilities.serializer_utilties import validate_model_uuid
from open.users.serializers import SimpleUserReadSerializer


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
            "name",
            "short_name",
            "is_liquid",
        )


class IngredientReadSerializer(ModelSerializer):
    user = SimpleUserReadSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes", "user")


class IngredientCreateSerializer(ModelSerializer):
    uuid = UUIDField(required=False, read_only=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes", "user")
        validators = [
            UniqueTogetherValidator(
                queryset=Ingredient.objects.all(), fields=["user", "name"]
            )
        ]

    def create(self, validated_data):
        create_model = self.Meta.model
        obj = create_model.objects.create(**validated_data)
        return obj


class IngredientUpdateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Ingredient
        fields = ("uuid", "notes", "name", "half_life_minutes", "user")

    # TODO - Need To Add Update


class IngredientCompositionReadSerializer(ModelSerializer):
    ingredient = IngredientReadSerializer()
    measurement = MeasurementReadSerializer()

    class Meta:
        model = IngredientComposition
        fields = ("uuid", "ingredient", "measurement", "quantity", "notes")
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientComposition.objects.all(),
                fields=["user", "ingredient", "measurement", "quantity"],
            )
        ]


class IngredientCompositionCreateSerializer(ModelSerializer):
    uuid = UUIDField(required=False, read_only=True)
    user = HiddenField(default=CurrentUserDefault())
    ingredient_uuid = UUIDField(source="ingredient.uuid")
    measurement_uuid = UUIDField(source="measurement.uuid")

    class Meta:
        model = IngredientComposition
        fields = ("uuid", "ingredient_uuid", "measurement_uuid", "quantity", "user")
        # the uniquetogether validator doesn't work with UUIDs
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=IngredientComposition.objects.all(), fields=["user", "ingredient", "measurement", "quantity"]
        #     )
        # ]

    def validate_ingredient_uuid(self, value):
        user = self.context["request"].user
        validate_model_uuid(Ingredient, uuid=value, user=user)
        return value

    def validate_measurement_uuid(self, value):
        validate_model_uuid(Measurement, uuid=value)
        return value

    def validate(self, validated_data):
        user = self.context["request"].user

        ingredient_uuid = validated_data.pop("ingredient")["uuid"]
        measurement_uuid = validated_data.pop("measurement")["uuid"]

        ingredient = Ingredient.objects.get(uuid=ingredient_uuid, user=user)
        measurement = Measurement.objects.get(uuid=measurement_uuid)

        validated_data["ingredient"] = ingredient
        validated_data["measurement"] = measurement

        if self.Meta.model.objects.filter(
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


class IngredientCompositionUpdateSerializer(ModelSerializer):
    ingredient_uuid = UUIDField(source="ingredient.uuid")
    measurement_uuid = UUIDField(source="measurement.uuid")

    class Meta:
        model = IngredientComposition
        fields = ("ingredient_uuid", "measurement_uuid", "quantity")

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

        return validated_data

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
