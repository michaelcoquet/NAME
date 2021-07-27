import datetime
import spotify.wrapper as spotify
from spotify.models import Track, Album
from account.models import Playlist


def build_playlists(social, playlists):
    track_list = []
    playlist_objs = []
    for playlist in playlists["items"]:
        if Playlist.objects.filter(id=playlist["id"]).count() == 0:
            playlist_tracks = [
                track["track"]
                for track in spotify.playlist_items(social, playlist["id"])["items"]
            ]
            playlist_tracks = build_tracks(social, playlist_tracks)
            playlist_obj = Playlist.objects.create(
                id=playlist["id"],
                data=playlist,
            )
            playlist_obj.tracks.set(playlist_tracks)
            playlist_obj.save()
            playlist_objs.append(playlist_obj)
    return playlist_objs


def build_tracks(social, tracks):
    track_list = []
    for track in tracks:
        if track != None:
            id = track["id"]
            # 1: check whether id already exists in db
            filter = Track.objects.filter(id=id)
            if filter.count() == 0:
                track_obj = Track.objects.create_track(
                    id=track["id"], data=track, social=social
                )
                track_list.append(track_obj)

    return track_list


def build_albums(social, albums):
    album_list = []
    for album in albums["items"]:
        track_list = build_tracks(social, album["album"]["tracks"]["items"])
        if Album.objects.filter(id=album["album"]["id"]).count() == 0:
            new_album = Album.objects.create(
                id=album["album"]["id"],
                data=album["album"],
            )
            new_album.tracks.set(track_list)
            album_list.append(new_album)

    return album_list
