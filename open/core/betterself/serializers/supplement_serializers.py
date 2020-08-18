from rest_framework.fields import (
    UUIDField,
    HiddenField,
    CurrentUserDefault,
    CharField,
    ListField,
)
from rest_framework.serializers import ModelSerializer

from open.core.betterself.models.ingredient_composition import IngredientComposition
from open.core.betterself.models.supplement import Supplement
from open.core.betterself.serializers.ingredient_composition_serializers import (
    IngredientCompositionReadSerializer,
)
from open.core.betterself.serializers.mixins import BaseModelReadSerializer
from open.core.betterself.serializers.validators import (
    ingredient_composition_uuid_validator,
)


class SimpleSupplementReadSerializer(ModelSerializer):
    class Meta:
        fields = ("uuid", "name")
        model = Supplement


class SupplementReadSerializer(BaseModelReadSerializer):
    # a bit of a heavy serializer because the nest goes deep, but keep for now
    # optimize later
    ingredient_compositions = IngredientCompositionReadSerializer(many=True)

    class Meta:
        model = Supplement
        fields = (
            "uuid",
            "created",
            "modified",
            "name",
            "notes",
            "ingredient_compositions",
            "display_name",
            "is_taken_with_food",
        )


class SupplementCreateUpdateSerializer(ModelSerializer):
    # don't use BaseCreateUpdateSerializer because we have
    # custom overrides on the many to many
    ingredient_composition_uuids = ListField(
        child=UUIDField(validators=[ingredient_composition_uuid_validator]),
        required=False,
    )
    uuid = UUIDField(required=False, read_only=True)
    user = HiddenField(default=CurrentUserDefault())
    notes = CharField(trim_whitespace=True, default="", allow_blank=True)

    class Meta:
        model = Supplement
        fields = (
            "uuid",
            "user",
            "ingredient_composition_uuids",
            "notes",
            "name",
            "is_taken_with_food",
        )

    def validate(self, validated_data):
        user = self.context["request"].user

        if "ingredient_composition_uuids" in validated_data:
            ingredient_compositions_uuids = validated_data.pop(
                "ingredient_composition_uuids"
            )
            ingredient_compositions = IngredientComposition.objects.filter(
                uuid__in=ingredient_compositions_uuids, user=user
            )
            validated_data["ingredient_compositions"] = ingredient_compositions

        return validated_data

    def create(self, validated_data):
        # many to many have to be set after the object is created
        ingredient_compositions = validated_data.pop("ingredient_compositions", [])

        create_model = self.Meta.model
        instance = create_model.objects.create(**validated_data)

        if ingredient_compositions:
            instance.ingredient_compositions.add(*ingredient_compositions)

        return instance

    def update(self, instance, validated_data):
        # many to many have to be set after the object is created
        ingredient_compositions = validated_data.pop("ingredient_compositions", [])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        if ingredient_compositions:
            instance.ingredient_compositions.add(*ingredient_compositions)

        return instance
