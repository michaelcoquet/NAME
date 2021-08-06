from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    # path("spotify-login/", views.spotify_login, name="spotify-login"),
    path("change_account/", views.change_account, name="change_account"),
    path("no_change/", views.no_change, name="no_change"),
    path("register/", views.register, name="register"),
    path("", include("django.contrib.auth.urls")),
    path("edit/", views.edit, name="edit"),
    path("users/", views.user_list, name="user_list"),
    path("users/<username>/", views.user_detail, name="user_detail"),
]
