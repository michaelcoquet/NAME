import datetime
from django.contrib.auth.decorators import login_required
import spotify.wrapper as spotify
from spotify.models import Album, Artist, Feature, Track, Genre
from account.models import Playlist, TopTrack, TopArtist, RecentTrack

# TODO: Implement batch api calls. The methods used here are slow
#       and can be improved by using spotify batch api calls where
#       available
# TODO: Unit testing
@login_required
def user_profile(social):
    # Profile.objects.filter(user=social.user).update()
    user_info = spotify.user_info(social)

    # Get all the users tracks
    playing_track = spotify.playing_track(social)
    if playing_track != None:
        playing_track_obj = build_track(social, playing_track["item"])

    track_list = []
    recent_tracks = spotify.recently_played_tracks(social)
    if recent_tracks != None:
        for t in recent_tracks["items"]:
            track_list.append(t["track"])
    recent_tracks_obj = build_recent_tracks(social, track_list)

    track_list = []
    saved_tracks = spotify.saved_tracks(social)
    if saved_tracks != None:
        for t in saved_tracks["items"]:
            track_list.append(t["track"])
    saved_tracks_obj = build_tracks(social, track_list)

    track_list = []
    top_tracks = spotify.top_tracks(social)
    if top_tracks != None:
        track_list = track_list + top_tracks["items"]
    top_tracks_obj = build_top_tracks(social, track_list)

    saved_album_list = []
    saved_albums = spotify.saved_albums(social)
    for item in saved_albums["items"]:
        saved_album_list.append(build_album(social, item["album"]))
        for album_track in item["album"]["tracks"]["items"]:
            album_track["album"] = item["album"]
            build_track(social, album_track)

    top_artists = spotify.top_artists(social)
    top_artists_obj = build_top_artists(social, top_artists["items"])

    top_genre_list = []
    seen = set(top_genre_list)
    for artist_obj in top_artists_obj:
        for genre in artist_obj.genres.values():
            if genre["name"] not in seen:
                seen.add(genre["name"])
                filtr = Genre.objects.filter(name=genre["name"])
                if filtr.count() == 0:
                    Genre.objects.create(name=genre["name"])
                top_genre_list.append(filtr.get())

    playlists = spotify.playlists(social)
    build_playlists(social, playlists)
    if playing_track != None:
        if playing_track_obj != None:
            social.user.profile.current_track = playing_track_obj
    if recent_tracks_obj != None:
        social.user.profile.recent_tracks.set(recent_tracks_obj)
    if saved_album_list != None:
        social.user.profile.saved_albums.set(saved_album_list)
    if saved_tracks_obj != None:
        social.user.profile.saved_tracks.set(saved_tracks_obj)
    if top_tracks_obj != None:
        social.user.profile.top_tracks.set(top_tracks_obj)
    if top_artists_obj != None:
        social.user.profile.top_artists.set(top_artists_obj)
    if top_genre_list != None:
        social.user.profile.top_genres.set(top_genre_list)
    social.user.profile.save()


def build_recent_tracks(social, tracks):
    track_list = []
    for i, track in enumerate(tracks):
        track_obj = build_recent_track(social, track, i)
        if track_obj != None:
            track_list.append(track_obj)
    return track_list


def build_recent_track(social, track, rank):
    if track != None:
        track_obj = build_track(social, track)

        RecentTrack.objects.create(
            owner=social.user.profile,
            track=track_obj,
            rank=rank,
        )

        return track_obj


def build_top_tracks(social, tracks):
    track_list = []
    for i, track in enumerate(tracks):
        track_obj = build_top_track(social, track, i)
        if track_obj != None:
            track_list.append(track_obj)
    return track_list


def build_top_track(social, track, rank):
    if track != None:
        track_obj = build_track(social, track)

        TopTrack.objects.create(
            owner=social.user.profile,
            track=track_obj,
            rank=rank,
        )

        return track_obj


def build_track(social, track):
    if track != None:
        id = track["id"]
        # 1: check whether id already exists in db
        filter = Track.objects.filter(id=id)
        if filter.count() == 1:
            return filter.get()
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
            return track_obj
    else:
        return None


def build_tracks(social, tracks):
    track_list = []
    for track in tracks:
        track_obj = build_track(social, track)
        if track_obj != None:
            track_list.append(track_obj)
    return track_list


def build_album(social, album):
    id = album["id"]
    filter = Album.objects.filter(id=id)
    if filter.count() == 1:
        return filter.get()
    elif filter.count() > 1:
        print("Error Album should be 0 or 1")
    else:
        album_obj = spotify.album(social=social, id=id)
        # the spotify api returns in the ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        # Here only the YYYY-MM-DD will be considered
        year = album_obj["release_date"][0:4]
        if year == "":
            year = 1  # default to 1
        month = album_obj["release_date"][5:7]
        if month == "":
            month = 1  # default to 1
        day = album_obj["release_date"][8:10]
        if day == "":
            day = 1  # if the api doesnt return a day then
            #          just give it 1
        date_obj = datetime.date(int(year), int(month), int(day))

        album_return = Album.objects.create(
            id=album_obj["id"],
            name=album_obj["name"],
            release_date=date_obj,
            total_tracks=album_obj["total_tracks"],
        )

        return album_return


def build_top_tracks(social, tracks):
    track_list = []
    for i, track in enumerate(tracks):
        track_obj = build_top_track(social, track, i)
        if track_obj != None:
            track_list.append(track_obj)
    return track_list


def build_top_track(social, track, rank):
    if track != None:
        track_obj = build_track(social, track)

        TopTrack.objects.create(
            owner=social.user.profile,
            track=track_obj,
            rank=rank,
        )

        return track_obj


def build_top_artists(social, artists):
    artist_obj_list = []
    for i, artist in enumerate(artists):
        artist_obj = build_top_artist(social, artist, i)
        if artist_obj != None:
            artist_obj_list.append(artist_obj)
    return artist_obj_list


def build_top_artist(social, artist, rank):
    if artist != None:
        artist_obj = build_artist(social, artist)

        TopArtist.objects.create(
            owner=social.user.profile, artist=artist_obj, rank=rank
        )

        return artist_obj


def build_artists(social, artists):
    artist_obj_list = []
    for artist in artists:
        artist_obj = build_artist(social, artist)
        artist_obj_list.append(artist_obj)

    return artist_obj_list


def build_artist(social, artist):
    id = artist["id"]
    filter = Artist.objects.filter(id=id)
    if filter.count() == 1:
        return filter.get()
    elif filter.count() > 1:
        print("Error count should be 0 or 1 for artists")
    else:
        artist_json = spotify.artist(social=social, id=id)

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

        return artist_obj


def build_feature(social, track):
    id = track["id"]
    filter = Track.objects.filter(id=id)
    if filter.count() == 1:
        return filter.get()
    elif filter.count() > 1:
        print("Error count should be 0 or 1 for Feature")
    else:
        feature_obj = spotify.feature(social, track["id"])
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


def build_playlists(social, playlists):
    all_tracks = []
    for item in playlists["items"]:
        track_obj_list = []
        playlist_tracks = spotify.playlist_items(social, item["id"])
        all_tracks = all_tracks + playlist_tracks["items"]
        for i, track in enumerate(all_tracks):
            track_obj_list.append(build_track(social, all_tracks[i]["track"]))

        new_playlist = Playlist.objects.create(
            id=item["id"],
            name=item["name"],
            owner=social.user.profile,
            public=item["public"],
            description=item["description"],
            collaborative=item["collaborative"],
        )

        new_playlist.tracks.set(track_obj_list)
