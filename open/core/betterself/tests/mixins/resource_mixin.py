from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework.test import APIClient

from open.users.factories import UserFactory
from open.users.models import User
from open.utilities.date_and_time import get_utc_now


class BetterSelfResourceViewTestCaseMixin(object):
    # need to have these attributes!
    url_name = None
    model_class_factory = None
    model_class = None

    @classmethod
    def setUpClass(cls):
        cls.url = reverse(cls.url_name)

        cls.current_time = get_utc_now()
        cls.current_time_isoformat = cls.current_time.isoformat()

        cls.current_date = cls.current_time.date()
        cls.current_date_isoformat = cls.current_date.isoformat()

        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        user_1 = UserFactory()
        user_2 = UserFactory()

        cls.user_1_id = user_1.id
        cls.user_2_id = user_2.id

        # create a few instances that will never be used
        cls.model_class_factory.create_batch(5)

        super().setUpTestData()

    def setUp(self):
        self.user_1 = User.objects.get(id=self.user_1_id)
        self.user_2 = User.objects.get(id=self.user_2_id)

        # a user that owns the instance
        self.client_1 = APIClient()
        self.client_1.force_login(self.user_1)

        # a user that shouldn't have access to the instance
        self.client_2 = APIClient()
        self.client_2.force_login(self.user_2)

        super().setUp()

    # TODO - separate these out into a seaparate mixin ..
    def test_view(self):
        self.model_class.objects.count()
        self.model_class_factory.create_batch(5, user=self.user_1)

        data = self.client_1.get(self.url).data
        self.assertEqual(len(data), 5)

    def test_no_access_view(self):
        self.model_class_factory(user=self.user_1)

        data = self.client_2.get(self.url).data
        self.assertEqual(len(data), 0)


class DeleteTestsMixin:
    def test_delete_view_on_non_uuid_url(self):
        response = self.client_1.delete(self.url)
        self.assertEqual(response.status_code, 405, response.data)

    def test_delete_view(self):
        instance = self.model_class_factory(user=self.user_1)
        instance_id = instance.id

        url = instance.get_update_url()

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, 204, response.data)

        with self.assertRaises(ObjectDoesNotExist):
            self.model_class.objects.get(id=instance_id)


class GetTestsMixin:
    def test_get_singular_resource(self):
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        response = self.client_1.get(url)
        data = response.data

        dynamic_generated_fields = ["generated_name", "display_name"]

        for key, value in data.items():
            if key in dynamic_generated_fields:
                continue

            instance_value = getattr(instance, key)
            if isinstance(instance_value, (str, bool)):
                # if the field stored on the db level is the right noe
                self.assertEqual(instance_value, value)

    def test_update_view_with_invalid_user_permission(self):
        """
        No one should be able to access other people's data
        """
        instance = self.model_class_factory(user=self.user_1)
        url = instance.get_update_url()

        params = {"notes": "fake spoof"}

        response = self.client_2.post(url, data=params)
        self.assertEqual(response.status_code, 404, response.data)
