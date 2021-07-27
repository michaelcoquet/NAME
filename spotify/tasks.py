import json
import spotify.wrapper as spotify
import spotify.functions as func
from django.core import serializers
from celery import shared_task

# TODO: Implement batch api calls to improve performance
# TODO: Unit testing
@shared_task
def scrape_user_profile(social_json):
    deserialize_json = serializers.deserialize("json", social_json)
    for social in deserialize_json:
        social.save()
    social = social.object

    # Get all the users tracks
    current_track = spotify.current_track(social)
    if current_track != None:
        current_track = func.build_tracks(social, [current_track["item"]])
        # track_list.append(current_track["item"])

    recent_tracks = spotify.recently_played_tracks(social)
    if recent_tracks != None:
        recent_tracks = func.build_tracks(
            social, [track["track"] for track in recent_tracks["items"]]
        )

    saved_tracks = spotify.saved_tracks(social)
    if saved_tracks != None:
        saved_tracks = func.build_tracks(
            social, [track["track"] for track in saved_tracks["items"]]
        )

    top_tracks = spotify.top_tracks(social)
    if top_tracks != None:
        top_tracks = func.build_tracks(social, top_tracks["items"])

    saved_albums = spotify.saved_albums(social)
    if saved_albums != None:
        saved_albums = func.build_albums(social, saved_albums)

    top_artists = spotify.top_artists(social)

    playlists = spotify.playlists(social)
    if playlists != None:
        playlists = func.build_playlists(social, playlists)

    top_genre_list = []
    seen = set(top_genre_list)
    for artist_json in top_artists["items"]:
        for genre in artist_json["genres"]:
            if genre not in seen:
                top_genre_list.append(genre)

    if current_track != None:
        social.user.profile.current_track = current_track[0]
    if recent_tracks != None:
        social.user.profile.recent_tracks.set(recent_tracks)
    if saved_tracks != None:
        social.user.profile.saved_tracks.set(saved_tracks)
    if top_tracks != None:
        social.user.profile.top_tracks.set(top_tracks)
    if saved_albums != None:
        social.user.profile.saved_albums.set(saved_albums)
    if top_artists != None:
        social.user.profile.top_artists = top_artists
    if top_genre_list != None:
        social.user.profile.top_genres = json.dumps(top_genre_list)
    if playlists != None:
        social.user.profile.playlists.set(playlists)

    social.user.profile.save()
    return None
