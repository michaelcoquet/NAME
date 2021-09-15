from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "data",
        "feature",
    ]
