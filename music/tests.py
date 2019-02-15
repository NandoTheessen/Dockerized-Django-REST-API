from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from .models import Song
from .serializers import SongsSerializer

# Create your tests here.


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_song(title="", artist=""):
        if title != "" and artist != "":
            Song.objects.create(title=title, artist=artist)

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def login_client(self, username="", password=""):
        # get a token from DRF
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )

        self.token = response.data['token']
        # set the token in the header
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )
        self.user.save()
        self.create_song("like glue", "sean paul")
        self.create_song("candy man", "kool savas")
        self.create_song("deine mutter", "kool savas")
        self.create_song("immer wieder", "mo trip")


class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # this is the update you need to add to the test, login
        self.login_client('test_user', 'testing')
        # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Song.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthRegisterUserTest(BaseViewTest):

    def test_register_a_user_with_valid_data(self):
        url = reverse(
            'auth-register',
            kwargs={
                "version": "v1"
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "username": "new_user",
                "password": "new_pass",
                "email": "new_user@email.com"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_a_user_with_invalid_data(self):

        url = reverse(
            'auth-register',
            kwargs={
                "version": "v1"
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "username": "",
                "password": "",
                "email": ""
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
