from django.urls import path
from .views import *


urlpatterns = [
    path("signup", SignupAPIView.as_view()),
    path("login", LoginAPIView.as_view()),
    path("info", UserInfoAPIView.as_view()),
    path("token_verify", JWTtokenVerifyView.as_view()),
]