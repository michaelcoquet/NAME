from django.urls import path, include
from django.contrib.auth import views

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("get-task-status/", views.get_task_status, name="get-task-status"),
    path("get_scraper_status/", views.get_scraper_status, name="get-scraper-status"),
    path("sync_spotify/", views.sync_spotify, name="sync_spotify"),
]
