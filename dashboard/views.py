import pandas as pd
import numpy as np
import plotly.express as px
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Profile
from spotify.models import Feature
import spotify.scraper as scrape


@login_required
def dashboard(request):
    profile_query = Profile.objects.filter(user=request.user)
    social_query = request.user.social_auth.filter(provider="spotify")

    if profile_query.count() == 1 and social_query.count() == 1:
        # returning user has spotify connnected
        print("TODO: build the graphs and whatever, possibly here")
    elif profile_query.count() == 1 and social_query.count() == 0:
        # returning user hasn't connected their Spotify account yet
        print("Error: user doesnt have a Spotify account linked yet")
    elif profile_query.count() == 0 and social_query.count() == 1:
        # first login is with Spotify, create a profile, mark their Spotify
        # account as connected, and scrape their Spotify data for the first
        # visuals
        Profile.objects.create(
            display_name=request.user.first_name,
            user=request.user,
            spotify_connected=True,
        )
        request.user.profile.spotify_connected = True
        Profile.objects.filter(user=request.user).update(spotify_connected=True)

        # Scrape Spotify API user data for the given user
        # to populate data for the dashboard
        # TODO: Use celery or something similar to do this
        #       async'ly
        scrape.user_profile(social_query.get())

    elif profile_query.count() == 0 and social_query.count() == 0:
        # first login must be with email or another method (if implemented)
        Profile.objects.create(
            display_name=request.user.first_name,
            user=request.user,
        )
    else:
        print("ERROR: something went horribly wrong in the dashboard view")

    profile_obj = request.user.profile.__repr__()
    radar_charts = build_radars(request.user.profile, profile_obj)
    histo_charts = build_histograms(profile_obj)

    return render(
        request,
        "dashboard/dashboard.html",
        {
            # "section": "dashboard"
            "profile": request.user.profile.__repr__(),
            "radar_charts": radar_charts,
            "histo_charts": histo_charts,
        },
    )


def build_radar_chart(data):
    labels = [
        "Danceability",
        "Energy",
        "Speechiness",
        "Acousticness",
        "Instrumentalness",
        "Liveness",
        "Valence",
    ]
    dataframe = pd.DataFrame(
        dict(
            r=data,
            theta=labels,
        )
    )
    fig = px.line_polar(dataframe, r="r", theta="theta", line_close=True)
    return fig.to_html(full_html=False)


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
    return fig.to_html(full_html=False)


# build_radars: returns a list of plotly html code to embed in dashboard.html
#               the datasource for each list element is as follows:
#                   charts[0] = current track
#                   charts[1] = tracks from saved albums
#                   charts[2] = liked tracks
#                   charts[3] = last 50 tracks
#                   charts[4] = last 25 tracks
#                   charst[5] = last 5 tracks
#                   charts[6] = top 50 tracks
#                   charts[7] = top 25 tracks
#                   charts[8] = top 5 tracks
#                   charts[9] = playlists
def build_radars(profile, profile_obj):

    charts = []  # the return list of plotly html code

    # 0 -- current track
    current_track = profile.current_track.__repr__(rank=0)
    charts.append(build_radar_chart(current_track.feature_repr))

    # 1 -- tracks from saved albums
    charts.append(build_radar_chart(profile_obj.album_tracks_analysis))

    # 2 -- liked tracks
    charts.append(build_radar_chart(profile_obj.liked_tracks_analysis))

    # 3 -- last 50 tracks
    charts.append(build_radar_chart(profile_obj.recent_tracks_analysis[0]))

    # 4 -- last 25 tracks
    charts.append(build_radar_chart(profile_obj.recent_tracks_analysis[1]))

    # 5 -- last 5 tracks
    charts.append(build_radar_chart(profile_obj.recent_tracks_analysis[2]))

    # 6 -- top 50 tracks
    charts.append(build_radar_chart(profile_obj.top_tracks_analysis[0]))

    # 7 -- top 25 tracks
    charts.append(build_radar_chart(profile_obj.top_tracks_analysis[1]))

    # 8 -- top 5 tracks
    charts.append(build_radar_chart(profile_obj.top_tracks_analysis[2]))

    # 9 -- playlists
    charts.append(build_radar_chart(profile_obj.playlist_tracks_analysis))

    return charts


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

    # # 1 -- liked tracks analysis
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

    # # 3 -- top tracks analysis
    # charts.append(build_bar_charts(top_tracks_analysis))

    # # 4 -- saved album tracks analysis
    # charts.append(build_bar_charts(saved_album_tracks_analysis))

    # # 0 -- all tracks analysis
    # charts.append(build_bar_charts(all_tracks_analysis))

    return charts
    # labels = [
    #     "Danceability",
    #     "Energy",
    #     "Key",
    #     "Loudness",
    #     "Mode",
    #     "Speechiness",
    #     "Acousticness",
    #     "Instrumentalness",
    #     "Liveness",
    #     "Valence",
    #     "Tempo",
    # ]
    # 1. collect track features for each scope below:
    #   - last 5 tracks
    #   - last 25 tracks
    #   - last 50 tracks
    #   - liked tracks
    #   - recent tracks
    #   - top tracks
    #   - saved album tracks
    #   - playlist tracks

    # last_5_track_features = []
    # last_25_track_features = []
    # recent_track_features = []
    # for i, track in enumerate(profile_obj.recent_tracks.values()):
    #     if track["feature_id"] == None:
    #         continue
    #     if i < 5:
    #         last_5_track_features.append(
    #             Feature.objects.filter(id=track["feature_id"]).get().__repr__("full")
    #         )
    #     if i >= 5 and i < 25:
    #         last_25_track_features.append(
    #             Feature.objects.filter(id=track["feature_id"]).get().__repr__("full")
    #         )
    #     if i >= 25 and i < 50:
    #         recent_track_features.append(
    #             Feature.objects.filter(id=track["feature_id"]).get().__repr__("full")
    #         )

    # last_25_track_features = last_5_track_features + last_25_track_features
    # recent_track_features = last_25_track_features + recent_track_features

    # last_5_dataframe = pd.DataFrame(last_5_track_features, columns=labels)
    # last_25_dataframe = pd.DataFrame(last_25_track_features, columns=labels)
    # last_50_dataframe = pd.DataFrame(recent_track_features, columns=labels)
    # last_dataframes = [last_50_dataframe, last_25_dataframe, last_5_dataframe]

    # bin_single = []
    # bins = []
    # data_single = []
    # data = []
    # for dataframe in last_dataframes:
    #     for i, metric in enumerate(dataframe):
    #         bin_single.append(
    #             np.linspace(
    #                 float(dataframe[metric].min()),
    #                 float(dataframe[metric].max()),
    #                 10,
    #                 dtype="int",
    #             ).tolist()
    #         )
    #         g = dataframe.groupby(
    #             pd.cut(dataframe[metric], bin_single[i], duplicates="drop")
    #         )
    #         data_single.append(g.count()[metric].tolist())
    #     data.append(data_single)
    #     bins.append(bin_single)
    #     data_single = []
    #     bin_single = []

    # return None
