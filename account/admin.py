from django.contrib import admin
from .models import Playlist, Profile, Image, TopTrack, RecentTrack


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
        "data",
    ]


@admin.register(TopTrack)
class TopTrackAdmin(admin.ModelAdmin):
    list_display = [
        "owner",
        "track",
        "rank",
    ]


@admin.register(RecentTrack)
class RecentTrackAdmin(admin.ModelAdmin):
    list_display = [
        "owner",
        "track",
        "rank",
    ]
