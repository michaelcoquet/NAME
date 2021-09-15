from django.urls import path
from . import views

urlpatterns = [
    path("admin/", views.db_admin, name="db_admin"),
]
