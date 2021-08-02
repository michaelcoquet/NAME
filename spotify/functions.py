import spotify.wrapper as spotify
from spotify.models import Track, Album
from account.models import Playlist, TopTrack, RecentTrack


def build_playlists(social, playlists):
    playlist_objs = []
    playlist_tracks = []
    playlist_track_ids = []
    for playlist in playlists:
        playlist_query = Playlist.objects.filter(id=playlist["id"])
        playlist_items_response = spotify.playlist_items(social, playlist["id"])
        playlist_tracks_json = [track["track"] for track in playlist_items_response]
        playlist_tracks_temp, track_ids_temp = build_tracks(playlist_tracks_json)
        if playlist_query.count() == 0:
            playlist_obj = Playlist.objects.create(
                id=playlist["id"],
                data=playlist,
            )
            playlist_obj.tracks.set(playlist_tracks_temp)
            playlist_obj.save()
        elif playlist_query.count() == 1:
            playlist_obj = playlist_query.get()
        else:
            playlist_obj = playlist_query.get()[0]
        playlist_objs.append(playlist_obj)
        playlist_tracks = playlist_tracks + playlist_tracks_temp
        playlist_track_ids = playlist_track_ids + track_ids_temp
    return playlist_objs, playlist_tracks, playlist_track_ids


def build_tracks(tracks):
    track_list = []
    track_ids = []
    for i, track in enumerate(tracks):
        if track != None and track["id"] != None:
            id = track["id"]
            # check whether id already exists in db
            filter = Track.objects.filter(id=id)
            if filter.count() == 0:
                track_obj = Track.objects.create(id=track["id"], data=track)
            elif filter.count() == 1:
                track_obj = filter.get()
                track_obj.rank = i
                track_obj.save()
            else:
                track_obj = filter.get()[0]
                track_obj.rank = i
                track_obj.save()
            track_list = track_list + [track_obj]
            track_ids = track_ids + [id]
    return track_list, track_ids


def build_tops(profile, tracks, type):
    track_list = []
    track_ids = []
    for i, track in enumerate(tracks):
        id = track["id"]
        filter_0 = Track.objects.filter(id=id)
        if filter_0.count() == 0:
            track_obj = Track.objects.create(id=track["id"], data=track)
        elif filter_0.count() == 1:
            track_obj = filter_0.get()
        else:
            track_obj = filter_0.get()[0]

        if type == "top":
            filter_1 = TopTrack.objects.filter(owner=profile, track=track_obj)
            if filter_1.count() == 0:
                TopTrack.objects.create(
                    owner=profile,
                    track=track_obj,
                    rank=i,
                )
        elif type == "recent":
            filter_1 = RecentTrack.objects.filter(owner=profile, track=track_obj)
            if filter_1.count() == 0:
                RecentTrack.objects.create(
                    owner=profile,
                    track=track_obj,
                    rank=i,
                )
        else:
            raise ("ERROR in build_tops invalid type")
        track_list = track_list + [track_obj]
        track_ids = track_ids + [id]
    return track_list, track_ids


def build_albums(albums):
    album_list = []
    album_tracks = []
    album_track_ids = []
    for album in albums:
        track_list, track_ids = build_tracks(album["album"]["tracks"]["items"])
        album_query = Album.objects.filter(id=album["album"]["id"])
        if album_query.count() == 0:
            new_album = Album.objects.create(
                id=album["album"]["id"],
                data=album["album"],
            )
            new_album.tracks.set(track_list)
        elif album_query.count() == 1:
            new_album = album_query.get()
        else:
            new_album = album_query.get()[0]

        album_list.append(new_album)
        album_track_ids = album_track_ids + track_ids
        album_tracks = album_tracks + track_list
    return album_list, album_tracks, album_track_ids
