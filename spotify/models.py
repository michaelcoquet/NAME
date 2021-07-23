import json
from django.db import models

# from account.models import Image


class Feature(models.Model):
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

    def __str__(self):
        return "TODO"

    def __repr__(self, size):
        base_features = [
            float(self.danceability) * 100,
            float(self.energy) * 100,
            float(self.speechiness) * 100,
            float(self.acousticness) * 100,
            float(self.instrumentalness) * 100,
            float(self.liveness) * 100,
            float(self.valence) * 100,
        ]
        if size == "full":
            # [danceability, energy, key, loudness, Mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo]
            full_features = [
                base_features[0],
                base_features[1],
                self.key,
                self.loudness,
                self.mode,
            ]
            full_features += base_features[2:]
            full_features.append(self.tempo)
            return full_features
        else:
            # [danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence]
            return base_features


class Genre(models.Model):
    name = models.CharField(primary_key=True, max_length=62)


class Album(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=200, null=True)
    release_date = models.DateField(blank=True, null=True)
    total_tracks = models.IntegerField()
    # tracks = models.ManyToOneRel()
    # tracks = models.ForeignKey(Track, on_delete=models.CASCADE, null=True)

    def get_genres(self):
        return "\n".join([genre.name for genre in self.genres.all()])


class Artist(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    genres = models.ManyToManyField(Genre)
    popularity = models.IntegerField()
    # images = models.ForeignKey(Image, on_delete=models.CASCADE)

    def get_genres(self):
        return "\n".join([genre.name for genre in self.genres.all()])

    def __str__(self):
        return f"{self.name}"


class Track(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=200, null=True)
    artists = models.ManyToManyField(Artist)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    disc_number = models.IntegerField()
    track_number = models.IntegerField()
    duration = models.IntegerField()
    feature = models.OneToOneField(Feature, on_delete=models.CASCADE, null=True)

    def to_json(self):
        artists = []
        for artist in self.artists.values():
            artists.append(artist["name"])
        track_dict = {
            "name": self.name,
            "artists": artists,
        }
        return json.dumps(track_dict)

    def __str__(self):
        artists_str = []
        for artist in self.artists.values():
            artists_str.append(artist["name"])
        return self.name + " --- " + ", ".join([artist for artist in artists_str])

    def __repr__(self, rank):
        self.rank = rank  # used for users top lists
        self.artists_repr = [artist["name"] for artist in self.artists.values()]
        self.feature_repr = self.feature.__repr__("base")
        return self
