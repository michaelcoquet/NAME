# Spotify API wrapper, this will handle all the API calls to Spotify
import requests, json, datetime
from django.contrib.auth.decorators import login_required
from spotify.models import Album, Artist, Feature, Track, Genre

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


def get_artist(social, id):
    url = "https://api.spotify.com/v1/artists/{}".format(id)
    response = build_get(url, get_token(social))
    return json.loads(response.text)


def get_album(social, id):
    url = "https://api.spotify.com/v1/albums/{}?market={}".format(id, market)
    response = build_get(url, get_token(social))
    return json.loads(response.text)


def get_feature(social, id):
    url = "https://api.spotify.com/v1/audio-features/{}".format(id)
    response = build_get(url, get_token(social))
    return json.loads(response.text)


@login_required
def build_user_profile(social):
    # Profile.objects.filter(user=social.user).update()
    user_info = get_user_info(social)

    # Get all the users tracks
    playing_track = get_playing_track(social)
    track_list = []
    if playing_track != None:
        track_list.append(playing_track["item"])

    saved_tracks = get_saved_tracks(social)
    if saved_tracks != None:
        for t in saved_tracks["items"]:
            track_list.append(t["track"])

    top_tracks = get_top_tracks(social)
    if top_tracks != None:
        track_list = track_list + top_tracks["items"]

    recent_tracks = get_recently_played_tracks(social)
    if recent_tracks != None:
        for t in recent_tracks["items"]:
            track_list.append(t["track"])

    build_tracks(social=social, tracks=track_list)

    saved_albums = get_saved_albums(social)

    top_artists = get_top_artists(social)

    playlists = get_playlists(social)
    print("done building profile")


def build_tracks(social, tracks):
    for track in tracks:
        id = track["id"]
        # 1: check whether id already exists in db
        filter = Track.objects.filter(id=id)
        if filter.count() == 1:
            print("Track already Exists")
        elif filter.count() > 1:
            print("Error count should be 0 or 1 for tacks")
        else:
            # add the artists to the db if they dont already exist
            artists = build_artists(social=social, artists=track["artists"])
            # add the albums to the db if they dont already exist
            album = build_album(social=social, album=track["album"])
            # add the features to the db if they dont already exist
            feature = build_feature(social=social, track=track)

            track_obj = Track.objects.create(
                id=id,
                name=track["name"],
                album=album,
                disc_number=track["disc_number"],
                track_number=track["track_number"],
                duration=track["duration_ms"],
                feature=feature,
            )

            track_obj.artists.set(artists)


def build_album(social, album):
    id = album["id"]
    filter = Album.objects.filter(id=id)
    if filter.count() == 1:
        print("Album already exists")
    elif filter.count() > 1:
        print("Error Album should be 0 or 1")
    else:
        album_obj = get_album(social=social, id=id)
        # the spotify api returns in the ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        # Here only the YYYY-MM-DD will be considered
        year = album_obj["release_date"][0:4]
        month = album_obj["release_date"][5:7]
        day = album_obj["release_date"][8:10]
        date_obj = datetime.date(int(year), int(month), int(day))

        album_return = Album.objects.create(
            id=album_obj["id"],
            name=album_obj["name"],
            release_date=date_obj,
            total_tracks=album_obj["total_tracks"],
        )

        return album_return


def build_artists(social, artists):
    artist_obj_list = []
    for artist in artists:
        id = artist["id"]
        filter = Artist.objects.filter(id=id)
        if filter.count() == 1:
            print("Artist already exists")
        elif filter.count() > 1:
            print("Error count should be 0 or 1 for artists")
        else:
            artist_json = get_artist(social=social, id=id)

            # add the genres to the db if they dont already exist
            genre_list = []
            for genre in artist_json["genres"]:
                filter = Genre.objects.filter(name=genre)
                if filter.count() == 0:
                    genre_list.append(Genre.objects.create(name=genre))
                elif filter.count() == 1:
                    genre_list.append(filter.get())

            artist_obj = Artist.objects.create(
                id=id,
                name=artist_json["name"],
                popularity=artist_json["popularity"],
            )

            artist_obj.genres.set(genre_list)
            artist_obj_list.append(artist_obj)

    return artist_obj_list


def build_feature(social, track):
    id = track["id"]
    filter = Track.objects.filter(id=id)
    if filter.count() == 1:
        print("Feature already exists")
    elif filter.count() > 1:
        print("Error count should be 0 or 1 for Feature")
    else:
        feature_obj = get_feature(social, track["id"])
        return Feature.objects.create(
            danceability=feature_obj["danceability"],
            energy=feature_obj["energy"],
            key=feature_obj["key"],
            loudness=feature_obj["loudness"],
            mode=feature_obj["mode"],
            speechiness=feature_obj["speechiness"],
            acousticness=feature_obj["acousticness"],
            instrumentalness=feature_obj["instrumentalness"],
            liveness=feature_obj["liveness"],
            valence=feature_obj["valence"],
            tempo=feature_obj["tempo"],
        )
