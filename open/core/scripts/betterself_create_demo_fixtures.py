"""
dpy runscript betterself_create_demo_fixtures
"""
from open.core.betterself.constants import DEMO_TESTING_ACCOUNT
from open.core.betterself.utilities.demo_user_factory_fixtures import (
    create_demo_fixtures_for_user,
)
from open.users.models import User


def run():
    user = User.objects.get(username=DEMO_TESTING_ACCOUNT)
    create_demo_fixtures_for_user(user)
