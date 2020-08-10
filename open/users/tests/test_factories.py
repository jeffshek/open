from test_plus import TestCase

from open.users.factories import UserFactory


class TestUserFactories(TestCase):
    def test_user_factory(self):
        email = "test@gmail.com"
        user = UserFactory(email=email)
        self.assertEqual(user.email, email)
