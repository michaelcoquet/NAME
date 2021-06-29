from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Image(models.Model):
    photo = models.ImageField(blank=True)

class Profile(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    display_name = models.CharField(max_length=32, default="User")
    followers = None
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ForeignKey(Image, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Profile for user {self.user.username}"

class Feature(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    danceability = models.DecimalField(max_digits=4, decimal_places=3)
    energy = models.DecimalField(max_digits=4, decimal_places=3)
    key = models.IntegerField()
    loudness = models.DecimalField(max_digits=4, decimal_places=2)
    mode = models.DecimalField(max_digits=4, decimal_places=3)
    speechiness = models.DecimalField(max_digits=4, decimal_places=3)
    acousticness = models.DecimalField(max_digits=4, decimal_places=3)
    instrumentalness = models.DecimalField(max_digits=7, decimal_places=6)
    liveness = models.DecimalField(max_digits=4, decimal_places=3)
    valence = models.DecimalField(max_digits=4, decimal_places=3)
    tempo = models.DecimalField(max_digits=6, decimal_places=3)
    
class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    # artists = 
    # album = 
    disc_number = models.IntegerField()
    track_number = models.IntegerField()
    duration = models.IntegerField()
    feature = models.OneToOneField(Feature, on_delete=models.CASCADE)
    
class Genre(models.Model):
    name = models.CharField(max_length=32, null=True)

class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE)
    release_date = models.DateField(blank=True, null=True)
    total_tracks = models.IntegerField()
    tracks = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)

class Artist(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    albums = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    tracks = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)
    genres = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    popularity = models.IntegerField()
    images = models.ForeignKey(Image, on_delete=models.CASCADE)

class Playlist(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    owner = models.CharField(max_length=62, null=True)
    public = models.BooleanField()
    description = models.CharField(max_length=128, null=True)
    collaborative = models.BooleanField()
    followers = None
    images = models.ForeignKey(Image, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track)
