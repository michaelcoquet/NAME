import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from account.tasks import analyze_profile
from account.models import Profile
import spotify.scraper as scrape
from common.decorators import ajax_required
from django.views.decorators.http import require_GET
from celery.result import AsyncResult
from django_celery_results.models import TaskResult
from social_django.utils import load_strategy
from common import redis_functions as cache


@login_required
def dashboard(request):
    profile_query = Profile.objects.filter(user=request.user)
    social_query = request.user.social_auth.filter(provider="spotify")

    if profile_query.count() == 1 and social_query.count() == 1:
        # returning user has spotify connnected
        # possibly need to do some caching here
        pass
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
        scrape_task_id = scrape.user_profile(social_query)
        return render(
            request,
            "dashboard/dashboard_loading.html",
            {
                "section": "dashboard",
                "profile": profile_query.values()[0],
                "scrape_task_id": scrape_task_id,
            },
        )

    elif profile_query.count() == 0 and social_query.count() == 0:
        # first login must be with email or another method (if implemented)
        Profile.objects.create(
            display_name=request.user.first_name,
            user=request.user,
        )
    else:
        print("ERROR: something went horribly wrong in the dashboard view")

    analyze_task_id = analyze_profile.delay(request.user.id)

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "section": "dashboard",
            "profile": profile_query.values()[0],
            "analyze_task_id": analyze_task_id,
        },
    )


@ajax_required
@require_GET
def get_scraper_status(request):
    task_id = request.GET.get("task_id", None)
    if task_id is not None:
        task = AsyncResult(task_id)
        while task.status != "SUCCESS":
            pass
        response_data = {
            "state": task.state,
        }
        TaskResult.objects.filter(task_id=task_id).delete()
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse("No job id given")


@ajax_required
@require_GET
def get_task_status(request):
    if "radars" in cache.db:
        top_lists = cache.get("top_lists")
        radar_charts = cache.get("radars")
        histo_charts = cache.get("histos")
        top_lists = json.loads(top_lists)
        radar_charts = json.loads(radar_charts)
        histo_charts = json.loads(histo_charts)
        all_track_count = request.user.profile.all_tracks.all().count()
        liked_track_count = request.user.profile.saved_tracks.all().count()
        recent_track_count = request.user.profile.recent_tracks.all().count()
        top_track_count = request.user.profile.top_tracks.all().count()
        saved_album_track_count = request.user.profile.saved_album_tracks.all().count()
        playlist_track_count = request.user.profile.playlist_tracks.all().count()
        response_data = {
            "state": "SUCCESS",
            # "result": task.result,
            "top_lists": top_lists,
            "radar_charts": radar_charts,
            "histo_charts": histo_charts,
            "all_track_count": all_track_count,
            "liked_track_count": liked_track_count,
            "recent_track_count": recent_track_count,
            "top_track_count": top_track_count,
            "saved_album_track_count": saved_album_track_count,
            "playlist_track_count": playlist_track_count,
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    task_id = request.GET.get("task_id", None)
    if task_id is not None:
        task = AsyncResult(task_id)
        while task.status != "SUCCESS":
            pass
        top_lists = task.result[0]
        radar_charts = task.result[1]
        histo_charts = task.result[2]
        all_track_count = request.user.profile.all_tracks.all().count()
        liked_track_count = request.user.profile.saved_tracks.all().count()
        recent_track_count = request.user.profile.recent_tracks.all().count()
        top_track_count = request.user.profile.top_tracks.all().count()
        saved_album_track_count = request.user.profile.saved_album_tracks.all().count()
        playlist_track_count = request.user.profile.playlist_tracks.all().count()
        response_data = {
            "state": task.state,
            "result": task.result,
            "top_lists": top_lists,
            "radar_charts": radar_charts,
            "histo_charts": histo_charts,
            "all_track_count": all_track_count,
            "liked_track_count": liked_track_count,
            "recent_track_count": recent_track_count,
            "top_track_count": top_track_count,
            "saved_album_track_count": saved_album_track_count,
            "playlist_track_count": playlist_track_count,
        }
        TaskResult.objects.filter(task_id=task_id).delete()
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse("No job id given.")


def sync_spotify(request):
    profile_query = Profile.objects.filter(user=request.user)
    social_query = request.user.social_auth.filter(provider="spotify")
    social_query.get().refresh_token(load_strategy())
    if profile_query.count() == 1 and social_query.count() == 1:
        scrape_task_id = scrape.user_profile(social_query)
        return render(
            request,
            "dashboard/dashboard_loading.html",
            {
                "section": "dashboard",
                "profile": profile_query.values()[0],
                "scrape_task_id": scrape_task_id,
            },
        )
