from django.urls import path
from .views import ListSongsView, LoginView, RegisterView


urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterView.as_view(), name="auth-register")
]
