from rest_framework.serializers import ModelSerializer

from open.users.models import User


class SimpleUserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "uuid",
        )
