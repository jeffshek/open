from django.contrib.auth import get_user_model
from test_plus import TestCase

from open.core.betterself.constants import DEMO_TESTING_ACCOUNT
from open.core.betterself.utilities.demo_user_factory_fixtures import (
    create_demo_fixtures_for_user,
)
from open.users.factories import UserFactory

User = get_user_model()

"""
python manage.py test --pattern="*test_demo_fixture_creation.py" --keepdb
"""


class TestDemoFixtureUtility(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory(username=DEMO_TESTING_ACCOUNT)

    @classmethod
    def setUpTestData(cls):
        user = UserFactory(username=DEMO_TESTING_ACCOUNT, email=DEMO_TESTING_ACCOUNT)
        create_demo_fixtures_for_user(user)

    # turned this off until i know what i want to do with it ...
    # def test_demo_fixture_with_supplement_and_compositions(self):
    #     user_supplements = Supplement.objects.filter(user=self.user)
    #     instance = user_supplements[0]
    #
    #     self.assertGreater(instance.ingredient_compositions.all().count(), 0)

    def test_demo_fixture_wont_make_for_valid_user(self):
        user = UserFactory(username="real@gmail.com", email="real@gmail.com")

        with self.assertRaises(ValueError):
            create_demo_fixtures_for_user(user)
