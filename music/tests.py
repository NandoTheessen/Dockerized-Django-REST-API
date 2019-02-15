from django.urls import reverse
from django.test import TestCase
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

    def setup(self):
        self.create_song("like glue", "sean paul")
        self.create_song("candy man", "kool savas")
        self.create_song("deine mutter", "kool savas")
        self.create_song("immer wieder", "mo trip")


class GetAllSongsTest(BaseViewTest):

    def test_get_all_songs(self):

        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )

        expected = Song.objects.all()
        serialized = SongsSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
