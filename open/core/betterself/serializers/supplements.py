from rest_framework.fields import UUIDField, HiddenField, CurrentUserDefault
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


class SupplementCreateSerializer(ModelSerializer):
    uuid = UUIDField(required=False, read_only=True)
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Supplement
        fields = (
            "uuid",
            "user",
        )

    def validate(self, validated_data):
        return

    def create(self, validated_data):
        create_model = self.Meta.model
        obj = create_model.objects.create(**validated_data)
        return obj


class SupplementUpdateSerializer(ModelSerializer):
    class Meta:
        model = Supplement
        fields = "user"

    def validate(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
