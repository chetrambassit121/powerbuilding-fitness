from django.contrib import admin
from django.urls import path

from .views import (
    UserAPIView,
    UserCreateAPIView,
    UserLoginAPIView,
    UserProfileAPIView,
    UserProfileUpdateAPIView,
    UserUpdateAPIView,
)

urlpatterns = [
    path(
        "register/", UserCreateAPIView.as_view(), name="register-api"
    ),  
    path("login/", UserLoginAPIView.as_view(), name="login-api"),  
    path("user/", UserAPIView.as_view(), name="user-api"),
    path("user/edit/<int:id>/", UserUpdateAPIView.as_view(), name="user-update-api"),
    path("user_profile/", UserProfileAPIView.as_view(), name="user-profile-api"),
    path(
        "user_profile/edit/<int:id>",
        UserProfileUpdateAPIView.as_view(),
        name="user-profile-api",
    ),
]
