import json
import spotify.wrapper as spotify
from django.db import models


# class TrackManager(models.Manager):
#     def save_feature(self, *args, **kwargs):
#         feature = kwargs.pop("feature", False)
#         self.save
#         return new_track


class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    data = models.JSONField()
    feature = models.JSONField(null=True)

    # objects = TrackManager()

    # def save(self, feature, *args, **kwargs):
    #     self.feature = feature
    #     super().save(*args, **kwargs)


class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    data = models.JSONField()
    tracks = models.ManyToManyField(Track, related_name="album_tracks")
