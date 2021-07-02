import sys
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from account.models import Profile


@login_required
def dashboard(request):
    try:
        if request.user.profile != None:
            user = get_object_or_404(User, id=request.user.id)
            try:
                social = user.social_auth.get(provider="spotify")
                # user has active spotify account
                request.user.profile.spotify_connected = True
                Profile.objects.filter(user=request.user).update(spotify_connected=True)

                # Scrape Spotify API user data for the given user
                # to populate data for the dashboards analytics

            except UserSocialAuth.DoesNotExist:
                print("Error: user doesnt have a Spotify account linked yet")
            except:
                print("Unexpected error:", sys.exc_info()[0])

        else:
            print("ERROR: unknown this should not be reachable")
    except Profile.DoesNotExist:
        if request.session._session["social_auth_last_login_backend"] == "spotify":
            Profile.objects.create(
                display_name=request.user.first_name,
                user=request.user,
                spotify_connected=True,
            )
        else:
            Profile.objects.create(
                display_name=request.user.first_name,
                user=request.user,
            )
    # else:
    #     print("ERROR: profile exists, but got some other error")
    return render(request, "dashboard/dashboard.html", {"section": "dashboard"})
