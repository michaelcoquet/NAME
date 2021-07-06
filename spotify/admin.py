from django.contrib import admin
from .models import Track, Album, Genre, Artist, Feature


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "album",
        "disc_number",
        "track_number",
        "duration",
        "feature",
    ]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "release_date",
        "total_tracks",
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "get_genres", "popularity"]


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = [
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
