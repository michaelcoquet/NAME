from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    display_name = models.CharField(max_length=32, default="User")
    # TODO: followers = None
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)
    
    def __str__(self):
        return f"Profile for user {self.user.username}"

class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    # artists = 
    # album = 
    disc_number = models.IntegerField()
    track_number = models.IntegerField()
    duration = models.IntegerField()
    features = None
    
class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    # artists = models.ForeignKey()
    name = models.CharField(max_length=62, null=True)
    genres = None
    release_date = models.DateField(blank=True, null=True)
    total_tracks = models.IntegerField()
    tracks = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)

class Genre(models.Model):
    name = models.CharField(max_length=32, null=True)

class Artist(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    albums = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    tracks = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    popularity = models.IntegerField()
    images = None

class Playlist(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    owner = models.CharField(max_length=62, null=True)
    public = models.BooleanField()
    description = models.CharField(max_length=128, null=True)
    collaborative = models.BooleanField()
    followers = None
    images = None
    tracks = models.ManyToManyField(Track)
