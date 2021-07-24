import datetime
import spotify.wrapper as spotify
from spotify.models import Album, Artist, Feature, Track, Genre
from account.models import Playlist, TopTrack, TopArtist, RecentTrack


def build_albums(albums):
    track_list = []
    for album in albums["items"]:
        track_list = track_list + album["album"]["tracks"]["items"]

    return track_list


def build_playlists(social, playlists):
    track_list = []
    for playlist in playlists["items"]:
        if Playlist.objects.filter(id=playlist["id"]).count() == 0:
            Playlist.objects.create(id=playlist["id"], data=playlist)
            playlist_tracks = [
                track["track"]
                for track in spotify.playlist_items(social, playlist["id"])["items"]
            ]
            track_list = track_list + playlist_tracks
    return track_list


def populate_artists(artists):
    for artist in artists:
        if Artist.objects.filter(id=artist["id"]).count() == 0:
            Artist.objects.create(id=artist["id"], data=artist)


def populate_album(album):
    if Album.objects.filter(id=album["id"]).count() == 0:
        Album.objects.create(id=album["id"], data=album)
        if "artists" in album:
            populate_artists(album["artists"])


def populate_feature(social, track):
    if Feature.objects.filter(id=track["id"]).count() == 0:
        feature = spotify.feature(social, track["id"])
        Feature.objects.create(id=track["id"], data=feature)


def populate_tracks(social, tracks):
    for track in tracks:
        if Track.objects.filter(id=track["id"]).count() == 0:
            Track.objects.create(id=track["id"], data=track)
            if "artists" in track:
                populate_artists(track["artists"])
            if "album" in track:
                populate_album(track["album"])
            populate_feature(social, track)
