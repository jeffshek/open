import pytz
from rest_auth.serializers import TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    CharField,
    CurrentUserDefault,
    HiddenField,
    UUIDField,
    ChoiceField,
)
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import check_password


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
    signed_up_from = CharField(
        write_only=True, min_length=8, required=False, default="", trim_whitespace=True
    )
    timezone_string = ChoiceField(
        choices=pytz.all_timezones, required=False, default="US/Eastern"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "signed_up_from", "timezone_string"]

    # TODO test - does this work with just username / no email, etc.

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")

        is_betterself_user = False
        if validated_data["signed_up_from"] == "betterself":
            is_betterself_user = True

        validated_data["is_betterself_user"] = is_betterself_user

        user = User.objects.create(username=username, **validated_data)
        user.set_password(password)
        user.save()

        return user


class UserDeleteSerializer(Serializer):
    # most of this is actually redundant, i don't need to have a validation step, but i do this
    # out of paranoia reasons that someone may delete their account by mistake
    password = CharField()
    user = HiddenField(default=CurrentUserDefault())
    uuid = UUIDField()

    def validate(self, data):
        user = data["user"]
        validated_password = check_password(data["password"], user.password)

        if not validated_password:
            raise ValidationError("Invalid Password Entered")

        validated_uuid = str(user.uuid) == str(data["uuid"])
        if not validated_uuid:
            raise ValidationError("Invalid UUID", str(user.uuid))

        validate_user = user.username != "demo-testing@senrigan.io"
        if not validate_user:
            raise ValidationError(
                f"This is a protected user and cannot be deleted. {user.username}"
            )

        return data
