from account.models import Profile


def connect_spotify(backend, user, response, *args, **kwargs):
    if backend.name == "spotify":
        profile = Profile.objects.filter(user=user)
        profile = profile.get()
        profile.spotify_connected = True
        profile.save()
