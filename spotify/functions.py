# Spotify API wrapper, this will handle all the API calls to Spotify
import requests, json
from django.contrib.auth.decorators import login_required
from account.models import Profile

market = "CA"  # TODO: not quite sure how to deal with this yet, possibly
#                      request the users location
time_range = "long_term"  # TODO: not sure again, but for now long_term is probably best
limit = "50"  # for top artists/tracks
offset = "0"


def build_get(url, token):
    headers = {
        "content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % (token),
    }
    response = requests.request("GET", url, headers=headers)
    return response


@login_required
def get_token(social):
    return social.access_token


@login_required
def get_user_info(social):
    response = build_get("https://api.spotify.com/v1/me", get_token(social))
    return json.loads(response.text)


@login_required
def get_playing_track(social):
    url = "https://api.spotify.com/v1/me/player/currently-playing?market={}".format(
        market
    )
    response = build_get(url, get_token(social))
    if response.status_code == 204 and response.reason == "No Content":
        # user is not currently playing a track, or the user has private session
        # enabled
        return None
    elif (
        response.status_code == 200 and response.text == "" and response.reason == "OK"
    ):
        # no available devices found
        return None
    elif (
        response.status_code == 200 and response.reason == "OK" and response.text != ""
    ):
        return json.loads(response.text)
    else:
        # some unknown possible error
        return None


@login_required
def get_saved_albums(social):
    url = "https://api.spotify.com/v1/me/albums?limit={}&market={}".format(
        limit, market
    )
    response = build_get(url, get_token(social))
    return json.loads(response.text)


@login_required
def get_saved_tracks(social):
    url = "https://api.spotify.com/v1/me/tracks?market={}".format(market)
    response = build_get(url, get_token(social))
    return json.loads(response.text)


@login_required
def get_top_artists(social):
    url = "https://api.spotify.com/v1/me/top/artists?time_range={}&limit={}".format(
        time_range, limit
    )
    response = build_get(url, get_token(social))
    return json.loads(response.text)


@login_required
def get_top_tracks(social):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range={}&limit={}".format(
        time_range, limit
    )
    response = build_get(url, get_token(social))
    return json.loads(response.text)


@login_required
def get_recently_played_tracks(social):
    url = "https://api.spotify.com/v1/me/player/recently-played?limit={}".format(limit)
    response = build_get(url, get_token(social))
    return json.loads(response.text)


@login_required
def get_playlists(social):
    url = "https://api.spotify.com/v1/me/playlists?limit={}&offset={}".format(
        limit, offset
    )
    response = build_get(url, get_token(social))
    return json.loads(response.text)


@login_required
def build_user_profile(social):
    # Profile.objects.filter(user=social.user).update()
    user_info = get_user_info(social)
    playing_track = get_playing_track(social)
    saved_albums = get_saved_albums(social)
    saved_tracks = get_saved_tracks(social)
    top_artists = get_top_artists(social)
    top_tracks = get_top_tracks(social)
    recent_tracks = get_recently_played_tracks(social)
    playlists = get_playlists(social)
    print("done building profile")
