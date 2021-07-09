from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from spotify.models import Track


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

    def __str__(self):
        return f"Profile for user {self.user.username}"


class Playlist(models.Model):
    id = models.CharField(primary_key=True, max_length=62)
    name = models.CharField(max_length=62, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    public = models.BooleanField()
    description = models.CharField(max_length=128, null=True)
    collaborative = models.BooleanField()
    followers = None
    images = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    tracks = models.ManyToManyField(Track)


# user_model = get_user_model()
# user_model.add_to_class(
#     "following",
#     models.ManyToManyField(
#         "self", through=Contact, related_name="followers", symmetrical=False
#     ),
# )
