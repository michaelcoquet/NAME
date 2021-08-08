from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls.conf import re_path

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
    # re_path(
    #     r"^register-by-token/(?P<backend>[^/]+)/$",
    #     views.register_by_access_token,
    #     name="register_by_acces_token",
    # ),
]
