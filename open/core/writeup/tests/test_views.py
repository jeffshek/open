from django.test import TestCase
from rest_framework.reverse import reverse

from open.users.factories import UserFactory


class WriteupViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_this_point(self):
        print("yep")
