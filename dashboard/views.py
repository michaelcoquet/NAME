import sys
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth

from account.models import Profile
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

    radar_labels = [
        "Danceability",
        "Energy",
        "Speechiness",
        "Acousticness",
        "Instrumentalness",
        "Liveness",
        "Valence",
    ]
    current_track = request.user.profile.current_track.__repr__(0)
    current_track_dict = {}
    current_track_dict["name"] = (
        current_track.name + " --- " + ", ".join(current_track.artists_repr)
    )
    current_track_dict["feature_repr"] = current_track.feature_repr

    profile_obj = request.user.profile.__repr__()
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
    return render(
        request,
        "dashboard/dashboard.html",
        {
            # "section": "dashboard"
            "radar_labels": radar_labels,
            "current_track": current_track_dict,
            "profile": profile_obj,
            "profile_dict": profile_dict,
        },
    )
