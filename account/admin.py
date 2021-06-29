from django.contrib import admin
from .models import Profile, Track, Album, Genre, Artist, Playlist, Feature, Image


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "disc_number", "track_number", "duration", "feature"]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "genres", "release_date", "total_tracks", "tracks"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "albums", "tracks", "genres", "popularity", "images"]


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


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["photo"]
