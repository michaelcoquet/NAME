from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Profile


@login_required
def dashboard(request):
    try:
        if request.user.profile != None:
            try:
                if request.session._session["spotify_state"] != None:
                    request.user.profile.spotify_connected = True
                    # Profile.objects.filter(user=request.user).update(
                    #     spotify_connected=True
                    # )
                    print("Spotify Account Succesfully Associated")
                else:
                    print("ERROR: unknown this should not be reachable")
            except:
                print("No Spotify account associated continue as a guest")
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
    return render(request, "account/dashboard.html", {"section": "dashboard"})
