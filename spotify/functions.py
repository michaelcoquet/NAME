import datetime
import spotify.wrapper as spotify
from spotify.models import Track, Album
from account.models import Playlist


def build_playlists(social, playlists):
    playlist_objs = []
    playlist_tracks = []
    playlist_track_ids = []
    for playlist in playlists["items"]:
        if Playlist.objects.filter(id=playlist["id"]).count() == 0:
            playlist_tracks_json = [
                track["track"]
                for track in spotify.playlist_items(social, playlist["id"])["items"]
            ]
            playlist_tracks_temp, track_ids_temp = build_tracks(playlist_tracks_json)
            playlist_tracks = playlist_tracks + playlist_tracks_temp
            playlist_track_ids = playlist_track_ids + track_ids_temp
            playlist_obj = Playlist.objects.create(
                id=playlist["id"],
                data=playlist,
            )
            playlist_obj.tracks.set(playlist_tracks_temp)
            playlist_obj.save()
            playlist_objs.append(playlist_obj)
    return playlist_objs, playlist_tracks, playlist_track_ids


def build_tracks(tracks):
    track_list = []
    track_ids = []
    for i, track in enumerate(tracks):
        if track != None:
            id = track["id"]
            # check whether id already exists in db
            filter = Track.objects.filter(id=id)
            if filter.count() == 0:
                track_obj = Track.objects.create(id=track["id"], data=track, rank=i)
                track_list = track_list + [track_obj]
                track_ids = track_ids + [id]
    return track_list, track_ids


def build_albums(social, albums):
    album_list = []
    album_tracks = []
    album_track_ids = []
    for album in albums["items"]:
        track_list, track_ids = build_tracks(album["album"]["tracks"]["items"])
        if Album.objects.filter(id=album["album"]["id"]).count() == 0:
            new_album = Album.objects.create(
                id=album["album"]["id"],
                data=album["album"],
            )
            new_album.tracks.set(track_list)
            album_list.append(new_album)
            album_track_ids = album_track_ids + track_ids
            album_tracks = album_tracks + track_list
    return album_list, album_tracks, album_track_ids


def build_features(social, tracks, track_ids):
    features = []
    # make sure the lists have equal length
    if len(tracks) == len(track_ids):
        features = spotify.features(social, track_ids)

        for i, track in enumerate(tracks):
            track.feature = features[i]
            track.save()
        print("done building features")
    else:
        raise ("build_features error list sizes dont match")
