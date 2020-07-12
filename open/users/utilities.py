from open.users.models import User

from rest_framework.authtoken.models import Token


def create_user_api_tokens():
    users = User.objects.all()
    for user in users:
        Token.objects.get_or_create(user=user)
