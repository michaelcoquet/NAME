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
        current_track, current_id = func.build_tracks([current_track["item"]])
        # track_list.append(current_track["item"])

    recent_tracks = spotify.recently_played_tracks(social)
    if recent_tracks != None:
        recent_tracks, recent_ids = func.build_tracks(
            [track["track"] for track in recent_tracks["items"]]
        )

    saved_tracks = spotify.saved_tracks(social)
    if saved_tracks != None:
        saved_tracks, saved_ids = func.build_tracks(
            [track["track"] for track in saved_tracks["items"]]
        )

    top_tracks = spotify.top_tracks(social)
    if top_tracks != None:
        top_tracks, top_ids = func.build_tracks(top_tracks["items"])

    album_tracks = []
    saved_albums = spotify.saved_albums(social)
    if saved_albums != None:
        saved_albums, album_tracks, album_ids = func.build_albums(social, saved_albums)

    top_artists = spotify.top_artists(social)

    playlist_tracks = []
    playlists = spotify.playlists(social)
    if playlists != None:
        playlists, playlist_tracks, playlist_ids = func.build_playlists(
            social, playlists
        )

    top_genre_list = []
    seen = set(top_genre_list)
    for artist_json in top_artists["items"]:
        for genre in artist_json["genres"]:
            if genre not in seen:
                top_genre_list.append(genre)

    all_tracks = []
    all_ids = []

    if current_track != None:
        social.user.profile.current_track = current_track[0]
        all_tracks = all_tracks + current_track
        all_ids = all_ids + current_id
    if recent_tracks != None:
        social.user.profile.recent_tracks.set(recent_tracks)
        all_tracks = all_tracks + recent_tracks
        all_ids = all_ids + recent_ids
    if saved_tracks != None:
        social.user.profile.saved_tracks.set(saved_tracks)
        all_tracks = all_tracks + saved_tracks
        all_ids = all_ids + saved_ids
    if top_tracks != None:
        social.user.profile.top_tracks.set(top_tracks)
        all_tracks = all_tracks + top_tracks
        all_ids = all_ids + top_ids
    if saved_albums != None:
        social.user.profile.saved_albums.set(saved_albums)
        all_tracks = all_tracks + album_tracks
        all_ids = all_ids + album_ids
    if top_artists != None:
        social.user.profile.top_artists = top_artists
    if top_genre_list != None:
        social.user.profile.top_genres = json.dumps(top_genre_list)
    if playlists != None:
        social.user.profile.playlists.set(playlists)
        all_tracks = all_tracks + playlist_tracks
        all_ids = all_ids + playlist_ids

    func.build_features(social, all_tracks, all_ids)

    social.user.profile.save()
    return None
