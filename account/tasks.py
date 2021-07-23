import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.core import serializers
from spotify.models import Feature, Artist, Track
from spotify import analyzer
from account.models import TopArtist, TopTrack, RecentTrack, Playlist
from celery import shared_task

top_n = 5  # the top number of songs or artists to return


def expand_queryset(track_queryset, key, n):
    track_objs = []
    for i, track in enumerate(track_queryset):
        track_obj = Track.objects.filter(id=track[key]).get()
        # exclude the track if there is no available analysis for it
        if track_obj.feature_id != None:
            if n != 0:
                if i < n:
                    track_objs.append(track_obj.__repr__(rank=(i + 1)))
                else:
                    pass
            else:
                track_objs.append(track_obj.__repr__(rank=(i + 1)))

    return track_objs


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
def build_radars(profile_obj, analyses):
    charts = []  # the return list of plotly html code

    # charts[0] -- current track
    if profile_obj.current_track != None:
        current_track = profile_obj.current_track.__repr__(0)
        charts.append(build_radar_chart([current_track.feature_repr]))
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
def build_histograms(profile_obj):
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
    for track in profile_obj.recent_tracks.values():
        if track["feature_id"] == None:
            continue
        else:
            recent_track_features.append(
                Feature.objects.filter(id=track["feature_id"]).get().__repr__("full")
            )
    recent_dataframe = pd.DataFrame(recent_track_features, columns=metrics)

    charts.append(build_bar_charts(metrics, recent_dataframe))

    return charts


@shared_task
def analyze_profile(profile_json):
    deserialize_json = serializers.deserialize("json", profile_json)
    for profile_obj in deserialize_json:
        profile_obj.save()
    profile_obj = profile_obj.object

    track_queryset = (
        TopTrack.objects.filter(owner=profile_obj).order_by("rank").values()
    )
    top_track_list = []
    top_track_objs = expand_queryset(track_queryset, "track_id", 0)
    top_5_tracks_analysis = analyzer.tracks_avg(top_track_objs[0:4])
    top_25_tracks_analysis = analyzer.tracks_avg(top_track_objs[0:24])
    top_50_tracks_analysis = analyzer.tracks_avg(top_track_objs[0:49])
    for track in top_track_objs[0:top_n]:
        top_track_list.append(track.to_json())

    track_queryset = (
        RecentTrack.objects.filter(owner=profile_obj).order_by("rank").values()
    )
    recent_track_objs = expand_queryset(track_queryset, "track_id", 0)
    last_5_tracks_analysis = analyzer.tracks_avg(recent_track_objs[0:4])
    last_25_tracks_analysis = analyzer.tracks_avg(recent_track_objs[0:24])
    last_50_tracks_analysis = analyzer.tracks_avg(recent_track_objs[0:49])

    liked_tracks = [track for track in profile_obj.saved_tracks.values()]
    liked_tracks_objs = expand_queryset(liked_tracks, "id", 0)
    liked_tracks_analysis = analyzer.tracks_avg(liked_tracks_objs)

    playlist_queryset = (
        Playlist.objects.filter(id=profile_obj.playlist_set.values()[0]["id"])
        .get()
        .tracks.values()
    )
    playlist_track_objs = expand_queryset(playlist_queryset, "id", 0)
    playlist_tracks_analysis = analyzer.tracks_avg(playlist_track_objs)

    album_tracks_objs = []
    for album in profile_obj.saved_albums.values():
        album_tracks_queryset = Track.objects.filter(album_id=album["id"]).values()
        album_tracks_objs = album_tracks_objs + expand_queryset(
            album_tracks_queryset, "id", 0
        )
    album_tracks_analysis = analyzer.tracks_avg(album_tracks_objs)

    top_artist_list = []
    artist_queryset = (
        TopArtist.objects.filter(owner=profile_obj).order_by("rank").values()[0:top_n]
    )
    for artist in artist_queryset:
        top_artist_list.append(
            Artist.objects.filter(id=artist["artist_id"]).get().__str__()
        )

    top_genre_list = [i[0] for i in profile_obj.top_genres.values_list()][
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

    radar_charts = build_radars(profile_obj, analyses)
    histo_charts = build_histograms(profile_obj)

    return top_lists, radar_charts, histo_charts
