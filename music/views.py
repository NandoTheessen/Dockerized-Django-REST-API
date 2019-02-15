from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.views import status

from rest_framework import generics, permissions
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

from .models import Song
from .serializers import SongsSerializer, TokenSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListSongsView(generics.ListAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Song.objects.all()
    serializer_class = SongsSerializer


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")

        if not username or not password or not email:
            return Response(
                data={
                    "message":
                    "username pw and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            new_user = User.objects.create_user(
                username=username, password=password, email=email
            )
            new_user.save()
        return Response(status=status.HTTP_201_CREATED)
