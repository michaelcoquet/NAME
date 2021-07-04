import sys
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth

from account.models import Profile
from spotify.functions import (
    get_user_info,
    get_playing_track,
    get_saved_albums,
    get_saved_tracks,
    get_top_artists,
    get_top_tracks,
    get_recently_played_tracks,
    get_playlists,
)


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
                # to populate data for the dashboard
                user_data = get_user_info(social)
                print("\n\n{}'s Profile:".format(user_data["display_name"]))
                current_track = get_playing_track(social)
                artists = []
                for artist in current_track["item"]["artists"]:
                    artists.append(artist["name"])
                print(
                    '\tCurrently Playing Track: "{}" by '.format(
                        current_track["item"]["name"]
                    ),
                    end="",
                )
                print(*artists, sep=", ")
                print("\temail: {}".format(user_data["email"]))
                print(
                    "\t# of Followers: {}\n\n".format(user_data["followers"]["total"])
                )
                print("\tSaved Albums: {}".format(get_saved_albums(social)))
                print("\tSaved Tracks: {}\n".format(get_saved_tracks(social)))
                print("\tTop Artists: {}".format(get_top_artists(social)))
                print("\tTop Tracks: {}\n".format(get_top_tracks(social)))
                print(
                    "\tRecently Played Tracks: {}\n".format(
                        get_recently_played_tracks(social)
                    )
                )
                print("\tPlaylists: {}\n\n".format(get_playlists(social)))
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
    except:
        print("Unexpected error:", sys.exc_info()[0])
    return render(request, "dashboard/dashboard.html", {"section": "dashboard"})
