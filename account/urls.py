from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("change_account/", views.change_account, name="change_account"),
    path("no_change/", views.no_change, name="no_change"),
    path("", include("django.contrib.auth.urls")),
]
