import json
import spotify.wrapper as spotify
import spotify.functions as func
from django.core import serializers
from celery import shared_task
from celery.result import AsyncResult
from django_celery_results.models import TaskResult
from django.conf import settings
from django.core.cache import cache
from spotify.models import Track
from csv import reader

# TODO: Unit testing


@shared_task
def scrape_current_track(social):
    social = deserialize(social)
    current_track = spotify.current_track(social)
    if current_track != None:
        current_track, current_id = func.build_tracks([current_track["item"]])
        social.user.profile.current_track = current_track[0]
        social.user.profile.save()
        return current_id


@shared_task
def scrape_recent_tracks(social):
    social = deserialize(social)
    recent_tracks = spotify.recently_played_tracks(social)
    if recent_tracks != None:
        recent_tracks, recent_ids = func.build_tops(
            social.user.profile,
            [track["track"] for track in recent_tracks["items"]],
            "recent",
        )
        social.user.profile.recent_tracks.set(recent_tracks)
        return recent_ids


@shared_task
def scrape_saved_tracks(social):
    social = deserialize(social)
    saved_tracks = spotify.saved_tracks(social)
    if saved_tracks != None:
        saved_tracks, saved_ids = func.build_tracks(
            [track["track"] for track in saved_tracks]
        )
        social.user.profile.saved_tracks.set(saved_tracks)
        return saved_ids


@shared_task
def scrape_top_tracks(social):
    social = deserialize(social)
    top_tracks = spotify.top_tracks(social)
    if top_tracks != None:
        top_tracks, top_ids = func.build_tops(
            social.user.profile, top_tracks["items"], "top"
        )
        social.user.profile.top_tracks.set(top_tracks)
        return top_ids


@shared_task
def scrape_album_tracks(social):
    social = deserialize(social)
    album_tracks = []
    saved_albums = spotify.saved_albums(social)
    if saved_albums != None:
        saved_albums, album_tracks, album_ids = func.build_albums(saved_albums)
        social.user.profile.saved_albums.set(saved_albums)
        social.user.profile.saved_album_tracks.set(album_tracks)
        return album_ids


@shared_task
def scrape_playlists(social):
    social = deserialize(social)
    playlist_tracks = []
    playlists = spotify.playlists(social)
    if playlists != None:
        playlists, playlist_tracks, playlist_ids = func.build_playlists(
            social, playlists
        )
        social.user.profile.playlists.set(playlists)
        social.user.profile.playlist_tracks.set(playlist_tracks)
        return playlist_ids


@shared_task
def scrape_top_genres_artists(social):
    social = deserialize(social)
    top_artists = spotify.top_artists(social)
    top_genre_list = []
    seen = set(top_genre_list)
    for artist_json in top_artists["items"]:
        for genre in artist_json["genres"]:
            if genre not in seen:
                top_genre_list.append(genre)
    if top_genre_list != None:
        social.user.profile.top_artists = top_artists
        social.user.profile.top_genres = json.dumps(top_genre_list)
        social.user.profile.save()
    return top_artists, top_genre_list


@shared_task
def scrape_features(social, track_ids):
    social = deserialize(social)
    features = []
    all_tracks = []
    # make sure the lists have equal length
    if len(track_ids) > 0:
        features = spotify.features(social, track_ids)
        for i, track_id in enumerate(track_ids):
            track = Track.objects.get(id=track_id)
            track.feature = features[i]
            track.save()
            all_tracks.append(track)

        social.user.profile.all_tracks.set(all_tracks)
        social.user.profile.save()


def deserialize(social_json):
    deserialize_json = serializers.deserialize("json", social_json)
    for social in deserialize_json:
        social.save()
    return social.object


@shared_task
def scrape_user_profile(social_json):

    # clear the cache
    cache.delete("top_lists")
    cache.delete("radars")
    cache.delete("histos")

    # scrape current track task
    curr_track_task_id = scrape_current_track.delay(social_json)
    curr_track_task = AsyncResult(curr_track_task_id)

    # scrape recent track task
    recent_track_task_id = scrape_recent_tracks.delay(social_json)
    recent_track_task = AsyncResult(recent_track_task_id)

    # scrape saved tracks task
    saved_track_task_id = scrape_saved_tracks.delay(social_json)
    saved_track_task = AsyncResult(saved_track_task_id)

    # scrape top tracks task
    top_track_task_id = scrape_top_tracks.delay(social_json)
    top_track_task = AsyncResult(top_track_task_id)

    # scrape album tracks task
    album_track_task_id = scrape_album_tracks.delay(social_json)
    album_track_task = AsyncResult(album_track_task_id)

    # scrape playlist task
    playlist_track_task_id = scrape_playlists.delay(social_json)
    playlist_track_task = AsyncResult(playlist_track_task_id)

    # scrape top artists and genres task
    genres_track_task_id = scrape_top_genres_artists.delay(social_json)
    genres_track_task = AsyncResult(genres_track_task_id)

    all_ids = []

    tasks_complete = 0

    collected = [
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ]

    while 1:
        if curr_track_task.status == "SUCCESS" and not collected[0]:
            if curr_track_task.result != None:
                all_ids = all_ids + curr_track_task.result
            collected[0] = True
            tasks_complete += 1
        if recent_track_task.status == "SUCCESS" and not collected[1]:
            all_ids = all_ids + recent_track_task.result
            collected[1] = True
            tasks_complete += 1
        if saved_track_task.status == "SUCCESS" and not collected[2]:
            all_ids = all_ids + saved_track_task.result
            collected[2] = True
            tasks_complete += 1
        if top_track_task.status == "SUCCESS" and not collected[3]:
            all_ids = all_ids + top_track_task.result
            collected[3] = True
            tasks_complete += 1
        if album_track_task.status == "SUCCESS" and not collected[4]:
            all_ids = all_ids + album_track_task.result
            collected[4] = True
            tasks_complete += 1
        if playlist_track_task.status == "SUCCESS" and not collected[5]:
            all_ids = all_ids + playlist_track_task.result
            collected[5] = True
            tasks_complete += 1
        if genres_track_task.status == "SUCCESS" and not collected[6]:
            collected[6] = True
            tasks_complete += 1

        if tasks_complete == 7:
            break

    features_task = scrape_features.delay(social_json, all_ids)
    while features_task.status != "SUCCESS":
        pass

    return None


# scrape_tracks used, in conjunction with the csv list of artists
# obtained from the musicbrainz database (mbdb), mbdb can be set
# up to automatically update at given intervals so this scraper
# could also be set up to be triggered at given intervals to up
# date the data for new tracks (using something like celery beat)
# but for now this is just a snapsshot of the current spotify
# database crossed with the mbdb, new tracks can still be discovered
# through user interactions however
@shared_task
def scrape_tracks(csv_path):
    with open(csv_path, "r") as read_obj:
        csv_reader = reader(read_obj)
        n_artists = len(list(csv_reader))
        print(n_artists)
    return
