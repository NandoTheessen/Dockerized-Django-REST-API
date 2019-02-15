from rest_framework import serializers
from .models import Song


class SongsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("title", "artist")

    def update(self, instance, validate_data):
        instance.title = validate_data.get("title", instance.title)
        instance.artist = validate_data.get("artist", instance.artist)
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("username", "email")
