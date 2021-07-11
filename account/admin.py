from django.contrib import admin
from .models import Playlist, Profile, Image, TopTrack


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["photo"]


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "owner",
        "public",
        "description",
        "collaborative",
        "followers",
        "images",
    ]


@admin.register(TopTrack)
class TopTrackAdmin(admin.ModelAdmin):
    list_display = [
        "owner",
        "track",
        "rank",
    ]
