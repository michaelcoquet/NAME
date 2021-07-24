import spotify.wrapper as spotify
import spotify.functions as func
from django.core import serializers
from spotify.models import Genre
from celery import shared_task

# TODO: Implement batch api calls to improve performance
# TODO: Unit testing
@shared_task
def scrape_user_profile(social_json):
    deserialize_json = serializers.deserialize("json", social_json)
    for social in deserialize_json:
        social.save()
    social = social.object

    track_list = []
    # Get all the users tracks
    playing_track = spotify.playing_track(social)
    if playing_track != None:
        track_list.append(playing_track["item"])

    recent_tracks = spotify.recently_played_tracks(social)
    if recent_tracks != None:
        recent_tracks = [track["track"] for track in recent_tracks["items"]]
        track_list = track_list + recent_tracks

    saved_tracks = spotify.saved_tracks(social)
    if saved_tracks != None:
        saved_tracks = [track["track"] for track in saved_tracks["items"]]
        track_list = track_list + saved_tracks

    top_tracks = spotify.top_tracks(social)
    if top_tracks != None:
        track_list = track_list + top_tracks["items"]

    saved_albums = spotify.saved_albums(social)
    if saved_albums != None:
        track_list = track_list + func.build_albums(saved_albums)

    top_artists = spotify.top_artists(social)
    func.populate_artists(top_artists["items"])

    playlists = spotify.playlists(social)
    if playlists != None:
        track_list = track_list + func.build_playlists(social, playlists)

    func.populate_tracks(social, track_list)
    # func.build_playlists(social, playlists)
    # if playing_track != None:
    #     if playing_track_obj != None:
    #         social.user.profile.current_track = playing_track_obj
    # if recent_tracks_obj != None:
    #     social.user.profile.recent_tracks.set(recent_tracks_obj)
    # if saved_album_list != None:
    #     social.user.profile.saved_albums.set(saved_album_list)
    # if saved_tracks_obj != None:
    #     social.user.profile.saved_tracks.set(saved_tracks_obj)
    # if top_tracks_obj != None:
    #     social.user.profile.top_tracks.set(top_tracks_obj)
    # if top_artists_obj != None:
    #     social.user.profile.top_artists.set(top_artists_obj)
    # if top_genre_list != None:
    #     social.user.profile.top_genres.set(top_genre_list)
    social.user.profile.save()
    return None
