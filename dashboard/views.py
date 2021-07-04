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
    print_tracks,
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
                    '\tCurrently Playing Track: "{}" --- '.format(
                        current_track["item"]["name"]
                    ),
                    end="",
                )
                print(*artists, sep=", ")
                print("\temail: {}".format(user_data["email"]))
                print(
                    "\t# of Followers: {}\n\n".format(user_data["followers"]["total"])
                )
                albums = get_saved_albums(social)
                albums_list = []
                for item in albums["items"]:
                    albums_list.append("\t\t" + item["album"]["name"])
                print("\tSaved Albums: ")
                print(*albums_list, sep="\n")

                tracks = get_saved_tracks(social)
                track_list = []
                artists = []
                for item in tracks["items"]:
                    for artist in item["track"]["artists"]:
                        artists.append(artist["name"])
                    track_str = '\t\t"{}"'.format(item["track"]["name"])
                    track_str = track_str + " --- " + ", ".join(artists)
                    artists = []
                    track_list.append(track_str)

                print("\tSaved Tracks:")
                print(*track_list, sep="\n")

                top_artists = get_top_artists(social)
                top_artists_list = []
                for item in top_artists["items"]:
                    top_artists_list.append("\t\t" + item["name"])
                print("\n\tTop Artists:")
                print(*top_artists_list, sep="\n")

                top_tracks = get_top_tracks(social)
                print("\tTop Tracks:")
                print_tracks(top_tracks)

                recent_tracks = get_recently_played_tracks(social)
                print("\tRecently Played Tracks:")
                print_tracks(recent_tracks)

                print("\tPlaylists:")
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
