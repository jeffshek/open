from test_plus.test import TestCase

from open.users.factories import UserFactory


# dpy test core.writeup


class WriteupViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_this_point(self):
        print("yep")
