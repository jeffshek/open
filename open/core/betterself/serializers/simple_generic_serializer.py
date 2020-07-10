from rest_framework.serializers import ModelSerializer


def create_name_uuid_serializer(model):
    """ Dynamically creates a serializer with a minimum set of required
    fields, easier to do this can create lots of tiny serializers that
    are just the same but different Meta.models
    """

    class NameUUIDSerializer(ModelSerializer):
        class Meta:
            fields = ("uuid", "created", "modified", "name")

    NameUUIDSerializer.Meta.model = model
    return NameUUIDSerializer()
