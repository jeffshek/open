from rest_auth.serializers import TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from open.users.models import User


class SimpleUserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "uuid",
        )


class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "uuid",
            "signed_up_from",
            "date_joined",
            "username",
            "email",
            "created",
            "modified",
        )


class UserTokenSerializer(TokenSerializer):
    user = UserReadSerializer()

    class Meta:
        model = Token
        fields = ["key", "user"]


# TODO - this view and serializer is on hold as you figure out registration (later)
class UserCreateSerializer(ModelSerializer):
    username = CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    # need to make email optional ... prob should think through signup form a little
    email = CharField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=False
    )
    password = CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email"]

    # TODO test - does this work with just username / no email, etc.

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create(
            username=validated_data["username"], **validated_data
        )
        user.set_password(password)
        user.save()

        return user
