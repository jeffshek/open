from rest_framework.fields import (
    UUIDField,
    HiddenField,
    CurrentUserDefault,
    SerializerMethodField,
    CharField,
)
from rest_framework.serializers import ModelSerializer

from open.utilities.date_and_time import format_datetime_to_human_readable


class BaseModelReadSerializer(ModelSerializer):
    display_name = SerializerMethodField()

    def get_display_name(self, instance):
        if hasattr(instance, "name"):
            return instance.name
        else:
            model = self.Meta.model
            model_name = model._meta.verbose_name

            created = instance.created
            created_serialized = format_datetime_to_human_readable(created)

            display_name = f"{model_name} | Create Time: {created_serialized} UTC"
            return display_name


class BaseCreateUpdateSerializer(ModelSerializer):
    uuid = UUIDField(required=False, read_only=True)
    user = HiddenField(default=CurrentUserDefault())
    # if you don't have this when notes is sent with "null/none", database integrity has an issue
    # since serializers will try to input that into the db
    notes = CharField(
        default="", trim_whitespace=True, required=False, allow_blank=True,
    )

    def create(self, validated_data):
        create_model = self.Meta.model
        obj = create_model.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
