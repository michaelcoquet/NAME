import sys
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth

from account.models import Profile
from spotify.scraper import build_user_profile


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
        profile_data = build_user_profile(social_query.get())
        print(profile_data)

    elif profile_query.count() == 0 and social_query.count() == 0:
        # first login must be with email or another method (if implemented)
        Profile.objects.create(
            display_name=request.user.first_name,
            user=request.user,
        )
    else:
        print("ERROR: something went horribly wrong in the dashboard view")

    return render(request, "dashboard/dashboard.html", {"section": "dashboard"})
