from account.models import Profile


def connect_spotify(backend, user, response, *args, **kwargs):
    profile = Profile.objects.filter(user=user)
    if backend.name == "spotify" and profile.count() == 1:
        profile = profile.get()
        profile.spotify_connected = True
        profile.save()
