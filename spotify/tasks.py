import spotify.wrapper as spotify
import spotify.functions as func
from django.core import serializers
from spotify.models import Genre
from celery import shared_task

# TODO: Implement batch api calls to improve performance
# TODO: Unit testing
@shared_task
def get_user_profile(social_json):
    deserialize_json = serializers.deserialize("json", social_json)
    for social in deserialize_json:
        social.save()
    social = social.object

    # Get all the users tracks
    playing_track = spotify.playing_track(social)
    if playing_track != None:
        playing_track_obj = func.build_track(social, playing_track["item"])

    track_list = []
    recent_tracks = spotify.recently_played_tracks(social)
    if recent_tracks != None:
        for t in recent_tracks["items"]:
            track_list.append(t["track"])
    recent_tracks_obj = func.build_recent_tracks(social, track_list)

    track_list = []
    saved_tracks = spotify.saved_tracks(social)
    if saved_tracks != None:
        for t in saved_tracks["items"]:
            track_list.append(t["track"])
    saved_tracks_obj = func.build_tracks(social, track_list)

    track_list = []
    top_tracks = spotify.top_tracks(social)
    if top_tracks != None:
        track_list = track_list + top_tracks["items"]
    top_tracks_obj = func.build_top_tracks(social, track_list)

    saved_album_list = []
    saved_albums = spotify.saved_albums(social)
    for item in saved_albums["items"]:
        saved_album_list.append(func.build_album(social, item["album"]))
        for album_track in item["album"]["tracks"]["items"]:
            album_track["album"] = item["album"]
            func.build_track(social, album_track)

    top_artists = spotify.top_artists(social)
    top_artists_obj = func.build_top_artists(social, top_artists["items"])

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
    func.build_playlists(social, playlists)
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
