import pandas as pd
import numpy as np
from numpy import dtype
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

    radar_labels, current_track_dict, profile_obj, profile_dict = build_radars(
        request.user.profile
    )
    histo_bins, histo_data = build_histograms(request.user.profile)

    return render(
        request,
        "dashboard/dashboard.html",
        {
            # "section": "dashboard"
            "radar_labels": radar_labels,
            "current_track": current_track_dict,
            "profile": profile_obj,
            "profile_dict": profile_dict,
            "histo_bins": histo_bins,
            "histo_data": histo_data,
        },
    )


def build_radars(profile):
    radar_labels = [
        "Danceability",
        "Energy",
        "Speechiness",
        "Acousticness",
        "Instrumentalness",
        "Liveness",
        "Valence",
    ]
    current_track = profile.current_track.__repr__(0)
    current_track_dict = {}
    current_track_dict["name"] = (
        current_track.name + " --- " + ", ".join(current_track.artists_repr)
    )
    current_track_dict["feature_repr"] = current_track.feature_repr

    profile_obj = profile.__repr__()
    profile_dict = {}
    profile_dict["top_tracks_analysis"] = [
        profile_obj.top_tracks_analysis[0],
        profile_obj.top_tracks_analysis[1],
        profile_obj.top_tracks_analysis[2],
    ]
    profile_dict["recent_tracks_analysis"] = [
        profile_obj.recent_tracks_analysis[0],
        profile_obj.recent_tracks_analysis[1],
        profile_obj.recent_tracks_analysis[2],
    ]
    profile_dict["liked_tracks_analysis"] = profile_obj.liked_tracks_analysis

    profile_dict["playlist_tracks_analysis"] = profile_obj.playlist_tracks_analysis
    profile_dict["album_tracks_analysis"] = profile_obj.album_tracks_analysis

    return radar_labels, current_track_dict, profile_obj, profile_dict


def build_histograms(profile_obj):
    labels = [
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
    # 1. collect track features for each scope below:
    #   - last 5 tracks
    #   - last 25 tracks
    #   - last 50 tracks
    #   - liked tracks
    #   - recent tracks
    #   - top tracks
    #   - saved album tracks
    #   - playlist tracks
    last_5_track_features = []
    last_25_track_features = []
    last_50_track_features = []
    for i, track in enumerate(profile_obj.recent_tracks.values()):
        if i < 5:
            last_5_track_features.append(
                Feature.objects.filter(id=track["feature_id"]).get().__repr__("full")
            )
        if i >= 5 and i < 25:
            last_25_track_features.append(
                Feature.objects.filter(id=track["feature_id"]).get().__repr__("full")
            )
        if i >= 25 and i < 50:
            last_50_track_features.append(
                Feature.objects.filter(id=track["feature_id"]).get().__repr__("full")
            )

    last_25_track_features = last_5_track_features + last_25_track_features
    last_50_track_features = last_25_track_features + last_50_track_features

    last_5_dataframe = pd.DataFrame(last_5_track_features, columns=labels)
    last_25_dataframe = pd.DataFrame(last_25_track_features, columns=labels)
    last_50_dataframe = pd.DataFrame(last_50_track_features, columns=labels)
    last_dataframes = [last_50_dataframe, last_25_dataframe, last_5_dataframe]

    bin_single = []
    bins = []
    data_single = []
    data = []
    for dataframe in last_dataframes:
        for i, metric in enumerate(dataframe):
            bin_single.append(
                np.linspace(
                    float(dataframe[metric].min()),
                    float(dataframe[metric].max()),
                    10,
                    dtype="int",
                ).tolist()
            )
            g = dataframe.groupby(
                pd.cut(dataframe[metric], bin_single[i], duplicates="drop")
            )
            data_single.append(g.count()[metric].tolist())
        data.append(data_single)
        bins.append(bin_single)
        data_single = []
        bin_single = []

    return bins, data
