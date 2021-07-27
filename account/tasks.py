import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.core import serializers
import spotify
from spotify.models import Track
from spotify import analyzer
from account.models import TopArtist, TopTrack, RecentTrack, Playlist
from celery import shared_task

top_n = 5  # the top number of songs or artists to return


# def get_features(track_json_list, key):
#     features = []
#     for i, track in enumerate(track_json_list):
#         feature = Feature.objects.filter(id=track[key]).get()
#         # track_obj = Track.objects.filter(id=track[key]).get()
#         # exclude the track if there is no available analysis for it
#         # if track_obj.feature_id != None:
#         #     if n != 0:
#         #         if i < n:
#         #             track_objs.append(track_obj.__repr__(rank=(i + 1)))
#         #         else:
#         #             pass
#         #     else:
#         #         track_objs.append(track_obj.__repr__(rank=(i + 1)))

#     return features


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
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
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

        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
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
            feature["danceability"],
            feature["energy"],
            feature["speechiness"],
            feature["acousticness"],
            feature["instrumentalness"],
            feature["liveness"],
            feature["valence"],
        ]
        charts.append(build_radar_chart([feature]))
    else:
        charts.append(None)

    # charts[1] -- top tracks
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

    # charts[2] -- last tracks
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

    # charts[3] -- liked tracks
    charts.append(build_radar_chart([analyses[1]]))

    # charts[4] -- playlists
    charts.append(build_radar_chart([analyses[8]]))

    # charts[5] -- tracks from saved albums
    charts.append(build_radar_chart([analyses[0]]))

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


# build_histograms: returns a matrix of plotly html code to embed in dashboard.html
#               the datasource for each list element is as follows:
#
#   charts[0][0:10] = all tracks analysis
#   charts[1][0:10] = liked tracks analysis
#   charts[2][0:10] = recent tracks analysis
#   charts[3][0:10] = top tracks analysis
#   charts[4][0:10] = saved album tracks analysis
def build_histograms(profile):
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

    charts = []

    # 1 -- liked tracks analysis
    charts.append(build_bar_charts(["total_bill"], px.data.tips()))

    # 2 -- recent tracks analysis
    recent_track_features = []
    for track in profile.recent_tracks.values():
        if track["feature"] == None:
            continue
        else:
            feat = track["feature"]
            feat = [
                feat["danceability"],
                feat["energy"],
                feat["key"],
                feat["loudness"],
                feat["mode"],
                feat["speechiness"],
                feat["acousticness"],
                feat["instrumentalness"],
                feat["liveness"],
                feat["valence"],
                feat["tempo"],
            ]
            recent_track_features.append(feat)
    recent_dataframe = pd.DataFrame(recent_track_features, columns=metrics)

    charts.append(build_bar_charts(metrics, recent_dataframe))

    return charts


@shared_task
def analyze_profile(profile_json):
    deserialize_json = serializers.deserialize("json", profile_json)
    for profile in deserialize_json:
        profile.save()
    profile = profile.object

    top_track_list = []
    # track_features = get_features(profile.top_tracks, "")
    top_5_tracks_analysis = analyzer.tracks_avg(profile.top_tracks.values()[0:5])
    top_25_tracks_analysis = analyzer.tracks_avg(profile.top_tracks.values()[0:25])
    top_50_tracks_analysis = analyzer.tracks_avg(profile.top_tracks.values()[0:50])
    for track in profile.top_tracks.values()[0 : top_n + 1]:
        top_track_list.append(track)

    # recent_track_objs = get_features(profile.recent_tracks)
    last_5_tracks_analysis = analyzer.tracks_avg(profile.recent_tracks.values()[0:5])
    last_25_tracks_analysis = analyzer.tracks_avg(profile.recent_tracks.values()[0:25])
    last_50_tracks_analysis = analyzer.tracks_avg(profile.recent_tracks.values()[0:50])

    liked_tracks = profile.saved_tracks
    # liked_tracks_objs = get_features(liked_tracks, "id", 0)
    liked_tracks_analysis = analyzer.tracks_avg(liked_tracks.values())

    playlist_tracks = []
    for playlist in profile.playlists.all():
        playlist_tracks = playlist_tracks + [
            track for track in playlist.tracks.values()
        ]
    # playlist_track_objs = get_features(playlist_queryset, "id", 0)
    playlist_tracks_analysis = analyzer.tracks_avg(playlist_tracks)

    album_tracks_objs = []
    for album in profile.saved_albums.all():
        album_tracks_objs = album_tracks_objs + [
            track for track in album.tracks.values()
        ]
        # album_tracks_objs = album_tracks_objs + get_features(
        #     album_tracks_queryset, "id", 0
        # )
    album_tracks_analysis = analyzer.tracks_avg(album_tracks_objs)

    top_artist_list = profile.top_artists["items"][0:top_n]
    # for artist in artist_queryset:
    #     top_artist_list.append(
    #         Artist.objects.filter(id=artist["artist_id"]).get().__str__()
    #     )

    top_genre_list = json.loads(profile.top_genres)[
        0:11
    ]  # TODO: find a better way to condense this list

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
    top_lists = [top_artist_list, top_genre_list, top_track_list]

    radar_charts = build_radars(profile, analyses)
    histo_charts = build_histograms(profile)

    return top_lists, radar_charts, histo_charts
