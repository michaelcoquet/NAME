from django.urls import path, include
from django.contrib.auth import views

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("get-task-status/", views.get_task_status, name="get-task-status"),
]
