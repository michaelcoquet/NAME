# Spotify API wrapper, this will handle all the API calls to Spotify
import requests, json
from django.contrib.auth.decorators import login_required


def build_get(url, token):
    headers = {
        "content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % (token),
    }
    response = json.loads(requests.request("GET", url, headers=headers).text)
    return response


@login_required
def get_token(social):
    return social.access_token


@login_required
def get_user_info(social):
    return build_get("https://api.spotify.com/v1/me", get_token(social))


@login_required
def get_playing_track(social):
    market = "US"
    url = "https://api.spotify.com/v1/me/player/currently-playing?market={}".format(
        market
    )
    return build_get(url, get_token(social))


@login_required
def get_saved_albums(social):
    return None


@login_required
def get_saved_tracks(social):
    return None


@login_required
def get_top_artists(social):
    return None


@login_required
def get_top_tracks(social):
    return None


@login_required
def get_recently_played_tracks(social):
    return None


@login_required
def get_playlists(social):
    return None
