from open.users.factories import UserFactory


class TestMixins:
    def setUpDefault(self):
        self.registered_user = UserFactory()
        self.staff_user = UserFactory()
