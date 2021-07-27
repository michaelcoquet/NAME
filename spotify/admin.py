from django.contrib import admin
from .models import Track


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "data",
        "feature",
        # "name",
        # "album",
        # "disc_number",
        # "track_number",
        # "duration",
        # "feature",
    ]
