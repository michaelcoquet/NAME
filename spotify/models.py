import json
import spotify.wrapper as spotify
from django.db import models


class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    data = models.JSONField()
    feature = models.JSONField(null=True)


class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    data = models.JSONField()
    tracks = models.ManyToManyField(Track, related_name="album_tracks")
