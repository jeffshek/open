from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from test_plus import TestCase

from open.users.models import User

MOCK_USERNAME = "smokey-the-bear"
MOCK_PASSWORD = "only-you-can-stop-forest-firrraaaaahss"
MOCK_EMAIL = "cure-disease@gmail.com"

"""
dpy test open.users.tests --keepdb
"""


class TestUserRegistrationWithAPI(TestCase):
    def test_signup_process(self):
        url = reverse("rest_register")
        data = {
            "username": MOCK_USERNAME,
            "password": "machine-learning",
            "email": MOCK_EMAIL,
        }

        client = APIClient()
        response = client.post(url, data=data)

        # if successful, 201
        self.assertEqual(response.status_code, 201, response.data)

        user_exists = User.objects.filter(username=MOCK_USERNAME)
        self.assertTrue(user_exists)

    def test_signup_process_with_invalid_username(self):
        # create the user, so it shouldn't be creatable
        User.objects.create_user(username=MOCK_USERNAME)

        url = reverse("rest_register")
        data = {
            "username": MOCK_USERNAME,
            "password1": MOCK_PASSWORD,
            "password2": MOCK_PASSWORD,
            "email": MOCK_EMAIL,
        }

        client = APIClient()
        response = client.post(url, data=data)

        self.assertEqual(response.status_code, 400)
        # returned response.data should be
        # {'username': [ErrorDetail(string='A user with that username already exists.', code='invalid')]}
        self.assertTrue("username" in response.data)

    def test_login_process_with_wrong_password(self):
        User.objects.create_user(username=MOCK_USERNAME, password=MOCK_PASSWORD)

        url = reverse("rest_login")
        data = {"username": MOCK_USERNAME, "password": "dinoSAAAUR"}

        client = APIClient()
        response = client.post(url, data)

        self.assertEqual(response.status_code, 400)
        # response.data is {'non_field_errors': [ErrorDetail(string='Unable to log in
        # with provided credentials.', code='invalid')]}
        self.assertTrue("non_field_errors" in response.data)

    def test_login_process_with_correct_creds_username(self):
        created_user = User.objects.create_user(
            username=MOCK_USERNAME, password=MOCK_PASSWORD
        )

        url = reverse("rest_login")
        data = {"username": MOCK_USERNAME, "password": MOCK_PASSWORD}

        client = APIClient()
        response = client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("key" in response.data)

        key = response.data["key"]
        expected_key = Token.objects.get(user=created_user).key

        self.assertEqual(key, expected_key)

    def test_login_process_with_correct_creds_email(self):
        created_user = User.objects.create_user(
            username=MOCK_USERNAME, email=MOCK_EMAIL, password=MOCK_PASSWORD
        )

        url = reverse("rest_login")
        data = {"email": MOCK_EMAIL, "password": MOCK_PASSWORD}

        client = APIClient()
        response = client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("key" in response.data)

        key = response.data["key"]
        expected_key = Token.objects.get(user=created_user).key

        self.assertEqual(key, expected_key)
