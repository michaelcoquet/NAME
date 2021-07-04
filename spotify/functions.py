# Spotify API wrapper, this will handle all the API calls to Spotify
import requests, json
from django.contrib.auth.decorators import login_required

market = "CA"  # TODO: not quite sure how to deal with this yet, possibly
#                      request the users location
time_range = "long_term"  # TODO: not sure again, but for now long_term is probably best
limit = "50"  # for top artists/tracks


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
    url = "https://api.spotify.com/v1/me/player/currently-playing?market={}".format(
        market
    )
    return build_get(url, get_token(social))


@login_required
def get_saved_albums(social):
    url = "https://api.spotify.com/v1/me/albums?limit={}&market={}".format(
        limit, market
    )
    return build_get(url, get_token(social))


@login_required
def get_saved_tracks(social):
    url = "https://api.spotify.com/v1/me/tracks?market={}".format(market)
    return build_get(url, get_token(social))


@login_required
def get_top_artists(social):
    url = "https://api.spotify.com/v1/me/top/artists?time_range={}&limit={}".format(
        time_range, limit
    )
    return build_get(url, get_token(social))


@login_required
def get_top_tracks(social):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range={}&limit={}".format(
        time_range, limit
    )
    return build_get(url, get_token(social))


@login_required
def get_recently_played_tracks(social):
    url = "https://api.spotify.com/v1/me/player/recently-played?limit={}".format(limit)
    return build_get(url, get_token(social))


@login_required
def get_playlists(social):
    return None


def print_tracks(tracks):
    track_list = []
    artists = []
    for item in tracks["items"]:
        for artist in item["artists"]:
            artists.append(artist["name"])
        track_str = '\t\t"{}"'.format(item["name"])
        track_str = track_str + " --- " + ", ".join(artists)
        artists = []
        track_list.append(track_str)
    print(*track_list, sep="\n")
