from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    Me,
    Users,
    PublicUser,
    ChangePassword,
    LogIn,
    LogOut,
    JWTLogin,
    NaverLogin,
    KakaoLogin,
)

urlpatterns = [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
    path("change-password/", ChangePassword.as_view()),
    path("log-in/", LogIn.as_view()),
    path("log-out/", LogOut.as_view()),
    path("get-auth-token/", obtain_auth_token),
    path("jwt-login/", JWTLogin.as_view()),
    path("naver/", NaverLogin.as_view()),
    path("kakao/", KakaoLogin.as_view()),
    path("@<str:username>/", PublicUser.as_view()),
]
