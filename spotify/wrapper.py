# Spotify API wrapper, this will handle all the API calls to Spotify
import requests, json
from django.contrib.auth.decorators import login_required

market = "CA"  # TODO: not quite sure how to deal with this yet, possibly
#                      request the users location
time_range = "long_term"  # TODO: not sure again, but for now long_term is probably best
limit = "50"  # for top artists/tracks
offset = "0"

# TODO: Develop and implement a protocol to deal with
#       the spotify api call rate limiting.
#
#       According to the docs if too many api calls have
#       been made in too short a time the next call will
#       return a status code 429 with a Retry-After
#       header which represents the number of seconds
#       to wait before retrying
#       https://developer.spotify.com/documentation/web-api/
# TODO: Implement scraping all data with the spotify api cursor since
#       the max limit for any API call is 50 results you need to continue
#       calling until the next pointer is null to get all results
# TODO: Unit testing
def build_get(url, token):
    headers = {
        "content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer %s" % (token),
    }
    api_response = requests.request("GET", url, headers=headers)
    return api_response


@login_required
def token(social):
    return social.access_token


@login_required
def user_info(social):
    api_response = build_get("https://api.spotify.com/v1/me", token(social))
    return json.loads(api_response.text)


@login_required
def current_track(social):
    url = "https://api.spotify.com/v1/me/player/currently-playing?market={}".format(
        market
    )
    api_response = build_get(url, token(social))
    if api_response.status_code == 204 and api_response.reason == "No Content":
        # user is not currently playing a track, or the user has private session
        # enabled
        return None
    elif (
        api_response.status_code == 200
        and api_response.text == ""
        and api_response.reason == "OK"
    ):
        # no available devices found
        return None
    elif (
        api_response.status_code == 200
        and api_response.reason == "OK"
        and api_response.text != ""
    ):
        return json.loads(api_response.text)
    else:
        # some unknown possible error
        return None


@login_required
def saved_albums(social):
    url = "https://api.spotify.com/v1/me/albums?limit={}&market={}".format(
        limit, market
    )
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


@login_required
def saved_tracks(social):
    url = "https://api.spotify.com/v1/me/tracks?limit={}&market={}".format(
        limit, market
    )
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


@login_required
def top_artists(social):
    url = "https://api.spotify.com/v1/me/top/artists?time_range={}&limit={}".format(
        time_range, limit
    )
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


@login_required
def top_tracks(social):
    url = "https://api.spotify.com/v1/me/top/tracks?time_range={}&limit={}".format(
        time_range, limit
    )
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


@login_required
def recently_played_tracks(social):
    url = "https://api.spotify.com/v1/me/player/recently-played?limit={}".format(limit)
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


@login_required
def playlists(social):
    url = "https://api.spotify.com/v1/me/playlists?limit={}&offset={}".format(
        limit, offset
    )
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


def playlist_items(social, id):
    fields = "items(track(href%2C%20id%2C%20name%2C%20artists%2C%20album(href%2C%20id%2C%20name%2C%20release_date%2C%20total_tracks)%2C%20disc_number%2C%20track_number%2C%20duration_ms))"
    url = "https://api.spotify.com/v1/playlists/{}/tracks?market={}&fields={}&limit={}&offset={}".format(
        id, market, fields, limit, offset
    )
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


def artist(social, id):
    url = "https://api.spotify.com/v1/artists/{}".format(id)
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


def album(social, id):
    url = "https://api.spotify.com/v1/albums/{}?market={}".format(id, market)
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


def feature(social, id):
    url = "https://api.spotify.com/v1/audio-features/{}".format(id)
    api_response = build_get(url, token(social))
    return json.loads(api_response.text)


def features(social, ids):
    if len(ids) <= 100:
        ids = ",".join(ids)
        url = "https://api.spotify.com/v1/audio-features?ids={}".format(ids)
        api_response = build_get(url, token(social))
        return json.loads(api_response.text)
    else:
        api_responses = []
        id_chunks = split_list(ids, 100)
        for id_chunk in id_chunks:
            id_chunk_str = ",".join(id_chunk)
            url = "https://api.spotify.com/v1/audio-features?ids={}".format(
                id_chunk_str
            )
            api_response = build_get(url, token(social))
            api_response = json.loads(api_response.text)
            api_response = api_response["audio_features"]
            api_responses = api_responses + api_response
        return api_responses


def split_list(list, n):
    return [list[i : i + n] for i in range(0, len(list), n)]
