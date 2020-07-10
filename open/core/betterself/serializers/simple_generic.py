from rest_framework.serializers import ModelSerializer


def create_name_uuid_serializer(model):
    class NameUUIDSerializer(ModelSerializer):
        class Meta:
            fields = ("uuid", "created", "modified", "name")

    NameUUIDSerializer.Meta.model = model
    return NameUUIDSerializer
