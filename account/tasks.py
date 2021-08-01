import json
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.core import serializers
from spotify import analyzer
from celery import shared_task
from collections import Counter
from django.conf import settings
from .models import TopTrack, RecentTrack
from spotify.models import Track
from common import redis_functions as cache

top_n = settings.TOP_N  # the top number of songs or artists to return


def build_radar_chart(datasets):
    labels = [
        "Danceability",
        "Energy",
        "Speechiness",
        "Acousticness",
        "Instrumentalness",
        "Liveness",
        "Valence",
    ]
    if len(datasets) == 1:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=datasets[0], theta=labels, fill="toself"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        return fig.to_html(full_html=False, include_plotlyjs=False)
    elif len(datasets) > 1:
        fig = go.Figure()
        names = []
        for i, dataset in enumerate(datasets):
            if i == 0:
                if len(dataset) != len(datasets) - 1:
                    raise ("ERROR something went wrong")
                else:
                    names = dataset
            else:
                fig.add_trace(
                    go.Scatterpolar(
                        r=dataset, theta=labels, fill="toself", name=names[i - 1]
                    )
                )

        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        return fig.to_html(full_html=False, include_plotlyjs=False)


# build_radars: returns a list of plotly html code to embed in dashboard.html
#               the datasource for each list element is as follows:
#                    = current track
#                   analyses[0] = tracks from saved albums
#                   analyses[1] = liked tracks
#                   analyses[2] = last 50 tracks
#                   analyses[3] = last 25 tracks
#                   analyses[4] = last 5 tracks
#                   analyses[5] = top 50 tracks
#                   analyses[6] = top 25 tracks
#                   analyses[7] = top 5 tracks
#                   analyses[8] = playlists
def build_radars(profile, analyses):
    charts = []  # the return list of plotly html code

    # charts[0] -- current track
    if profile.current_track != None:
        feature = profile.current_track.feature
        feature = [
            feature["danceability"] * 100,
            feature["energy"] * 100,
            feature["speechiness"] * 100,
            feature["acousticness"] * 100,
            feature["instrumentalness"] * 100,
            feature["liveness"] * 100,
            feature["valence"] * 100,
        ]
        charts.append(build_radar_chart([feature]))
    else:
        charts.append(None)

    # charts[1] -- top tracks
    if analyses[5] != 0 and analyses[6] != 0 and analyses[7] != 0:
        charts.append(
            build_radar_chart(
                [
                    ["Top 50 Tracks", "Top 25 Tracks", "Top 5 Tracks"],
                    analyses[5],
                    analyses[6],
                    analyses[7],
                ]
            )
        )
    else:
        charts.append(None)

    # charts[2] -- last tracks
    if analyses[2] != 0 and analyses[3] != 0 and analyses[4] != 0:
        charts.append(
            build_radar_chart(
                [
                    ["Last 50 Tracks", "Last 25 Tracks", "Last 5 Tracks"],
                    analyses[2],
                    analyses[3],
                    analyses[4],
                ]
            )
        )
    else:
        charts.append(None)

    # charts[3] -- liked tracks
    if analyses[1] != 0:
        charts.append(build_radar_chart([analyses[1]]))
    else:
        charts.append(None)

    # charts[4] -- playlists
    if analyses[8] != 0:
        charts.append(build_radar_chart([analyses[8]]))
    else:
        charts.append(None)

    # charts[5] -- tracks from saved albums
    if analyses[0] != 0:
        charts.append(build_radar_chart([analyses[0]]))
    else:
        charts.append(None)

    return charts


def build_bar_charts(metrics, dataframe):
    chart_list = []
    for metric in metrics:
        chart_list.append(build_bar_chart(metric, dataframe))

    return chart_list


def build_bar_chart(metric, dataframe):
    fig = px.histogram(dataframe, x=metric)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="track count")
    return fig.to_html(full_html=False, include_plotlyjs=False)


def append_histo_chart(charts, tracks):
    metrics = [
        "Danceability",
        "Energy",
        "Key",
        "Loudness",
        "Mode",
        "Speechiness",
        "Acousticness",
        "Instrumentalness",
        "Liveness",
        "Valence",
        "Tempo",
    ]

    track_features = []
    for track in tracks:
        if track["feature"] == None:
            continue
        else:
            feat = track["feature"]
            feat = [
                feat["danceability"] * 100,
                feat["energy"] * 100,
                feat["key"],
                feat["loudness"],
                feat["mode"],
                feat["speechiness"] * 100,
                feat["acousticness"] * 100,
                feat["instrumentalness"] * 100,
                feat["liveness"] * 100,
                feat["valence"] * 100,
                feat["tempo"],
            ]
            track_features.append(feat)
    dataframe = pd.DataFrame(track_features, columns=metrics)

    if len(dataframe) > 0:
        charts.append(build_bar_charts(metrics, dataframe))
    else:
        charts.append(None)

    return charts


# build_histograms: returns a matrix of plotly html code to embed in dashboard.html
#               the datasource for each list element is as follows:
#
#   charts[0][0:10] = all tracks analysis
#   charts[1][0:10] = liked tracks analysis
#   charts[2][0:10] = recent tracks analysis
#   charts[3][0:10] = top tracks analysis
#   charts[4][0:10] = saved album tracks analysis
#   charts[5][0:10] = playlist tracks analysis
def build_histograms(profile):
    charts = []

    # 0 -- all tracks chart
    charts = append_histo_chart(charts, profile.all_tracks.values())

    # 1 -- liked tracks chart
    charts = append_histo_chart(charts, profile.saved_tracks.values())

    # 2 -- recent tracks chart
    charts = append_histo_chart(charts, profile.recent_tracks.values())

    # 3 -- top tracks chart
    charts = append_histo_chart(charts, profile.top_tracks.values())

    # 4 -- saved album tracks chart
    charts = append_histo_chart(charts, profile.saved_album_tracks.values())

    # 5 -- playlist tracks chart
    charts = append_histo_chart(charts, profile.playlist_tracks.values())

    return charts


def genre_occurrences(top_genres):
    genre_list = json.loads(top_genres)
    top_genres_list = []

    counts = Counter()
    words = re.compile(r".*")

    for genre in genre_list:
        counts.update(words.findall(genre.lower()))

    counts = counts.most_common()
    if len(counts) > 1:
        if counts[0][0] == "":
            top_genres_list = [item[0] for item in counts[1:]]
        else:
            top_genres_list = [item[0] for item in counts]
    return top_genres_list


@shared_task
def analyze_profile(profile_json):
    deserialize_json = serializers.deserialize("json", profile_json)
    for profile in deserialize_json:
        profile.save()
    profile = profile.object

    if "radars" not in cache.db:
        top_track_list = (
            TopTrack.objects.filter(owner=profile).values().order_by("rank")
        )
        top_track_list = [
            Track.objects.filter(id=track["track_id"]).values()[0]
            for track in top_track_list
        ]
        top_5_tracks_analysis = analyzer.tracks_avg(top_track_list[0:4])
        top_25_tracks_analysis = analyzer.tracks_avg(top_track_list[0:24])
        top_50_tracks_analysis = analyzer.tracks_avg(top_track_list[0:49])

        recent_track_list = (
            RecentTrack.objects.filter(owner=profile).values().order_by("rank")
        )
        recent_track_list = [
            Track.objects.filter(id=track["track_id"]).values()[0]
            for track in recent_track_list
        ]
        last_5_tracks_analysis = analyzer.tracks_avg(recent_track_list[0:4])
        last_25_tracks_analysis = analyzer.tracks_avg(recent_track_list[0:24])
        last_50_tracks_analysis = analyzer.tracks_avg(recent_track_list[0:49])

        liked_tracks = profile.saved_tracks
        liked_tracks_analysis = analyzer.tracks_avg(liked_tracks.values())

        playlist_tracks = []
        for playlist in profile.playlists.all():
            playlist_tracks = playlist_tracks + [
                track for track in playlist.tracks.values()
            ]

        playlist_tracks_analysis = analyzer.tracks_avg(playlist_tracks)

        album_tracks_objs = []
        for album in profile.saved_albums.all():
            album_tracks_objs = album_tracks_objs + [
                track for track in album.tracks.values()
            ]

        album_tracks_analysis = analyzer.tracks_avg(album_tracks_objs)

        top_artist_list = profile.top_artists["items"][0:top_n]

        top_genre_list = genre_occurrences(profile.top_genres)[0:top_n]

        # analyses[0] -- tracks from saved albums
        # analyses[1] -- liked tracks
        # analyses[2] -- last 50 tracks
        # analyses[3] -- last 25 tracks
        # analyses[4] -- last 5 tracks
        # analyses[5] -- top 50 tracks
        # analyses[6] -- top 25 tracks
        # analyses[7] -- top 5 tracks
        # analyses[8] -- playlists
        analyses = [
            album_tracks_analysis,
            liked_tracks_analysis,
            last_50_tracks_analysis,
            last_25_tracks_analysis,
            last_5_tracks_analysis,
            top_50_tracks_analysis,
            top_25_tracks_analysis,
            top_5_tracks_analysis,
            playlist_tracks_analysis,
        ]

        # top_lists[0] -- Top Artists
        # top_lists[1] -- Top Genres
        # top_lists[2] -- Top Tracks
        top_lists = [top_artist_list, top_genre_list, top_track_list[0:top_n]]

        radar_charts = build_radars(profile, analyses)
        histo_charts = build_histograms(profile)

        cache.set("top_lists", top_lists)
        cache.set("radars", radar_charts)
        cache.set("histos", histo_charts)

        return top_lists, radar_charts, histo_charts
    else:
        top_lists = cache.get("top_lists")
        radar_charts = cache.get("radars")
        histo_charts = cache.get("histos")
        top_lists = json.loads(top_lists)
        radar_charts = json.loads(radar_charts)
        histo_charts = json.loads(histo_charts)

        return top_lists, radar_charts, histo_charts
