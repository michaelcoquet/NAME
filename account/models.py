from django.core import serializers
from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

# from account.tasks import expand_queryset
from spotify.models import Artist, Track, Album, Genre


class Contact(models.Model):
    user_from = models.ForeignKey(
        "auth.User", related_name="rel_from_set", on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        "auth.User", related_name="rel_to_set", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class Image(models.Model):
    photo = models.ImageField(blank=True)


class Profile(models.Model):
    # id = models.CharField(primary_key=True, max_length=62)
    display_name = models.CharField(max_length=32, default="User")
    followers = None
    follower_count = models.IntegerField(default=0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    spotify_connected = models.BooleanField(null=True)
    current_track = models.ForeignKey(
        Track, on_delete=CASCADE, null=True, related_name="+"
    )
    recent_tracks = models.ManyToManyField(
        Track, related_name="+", through="RecentTrack"
    )
    saved_albums = models.ManyToManyField(Album)
    saved_tracks = models.ManyToManyField(Track, related_name="+")
    top_tracks = models.ManyToManyField(
        Track, related_name="profiles", through="TopTrack"
    )
    top_artists = models.ManyToManyField(
        Artist, related_name="profiles", through="TopArtist"
    )
    top_genres = models.ManyToManyField(Genre)


class TopTrack(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    rank = models.IntegerField()

    def __str__(self):
        return self.track.__str__()


class RecentTrack(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    rank = models.IntegerField()

    def __str__(self):
        return self.track.__str__()


class TopArtist(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    rank = models.IntegerField()

    def __str__(self):
        return self.artist.__str__()


class Playlist(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    data = models.JSONField(null=True)
    # name = models.CharField(max_length=62, null=True)
    # owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # public = models.BooleanField()
    # description = models.CharField(max_length=128, null=True)
    # collaborative = models.BooleanField()
    # followers = None
    # images = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    # tracks = models.ManyToManyField(Track)
