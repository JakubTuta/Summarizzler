from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

urlpatterns: list[URLPattern] = [
    path("user/me/", views.User.as_view(), name="user"),
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify_token"),
]
