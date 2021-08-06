import requests, json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.conf import settings
from common.decorators import ajax_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated " "successfully")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


# def social_auth_complete(request):
#     client_id = settings.SOCIAL_AUTH_SPOTIFY_KEY
#     client_secret = settings.SOCIAL_AUTH_SPOTIFY_SECRET
#     redirect_uri = settings.SPOTIFY_REDIRECT_URI
#     url = "https://accounts.spotify.com/api/token"
#     code = request.GET.get("code")
#     payload = {
#         "grant_type": "authorization_code",
#         "code": code,
#         "redirect_uri": redirect_uri,
#         "client_id": client_id,
#         "client_secret": client_secret,
#     }
#     api_response = requests.post(url, data=payload)
#     api_response = json.loads(api_response.text)
#     access_token = api_response.get("access_token")
#     print(access_token)


# def spotify_login(request):
#     client_id = settings.SOCIAL_AUTH_SPOTIFY_KEY
#     response_type = "code"
#     redirect_uri = settings.SPOTIFY_REDIRECT_URI
#     scope = settings.SOCIAL_AUTH_SPOTIFY_SCOPE
#     scope = " ".join(scope)
#     params = {
#         "client_id": client_id,
#         "response_type": response_type,
#         "redirect_uri": redirect_uri,
#         "scope": scope,
#     }
#     url = "https://accounts.spotify.com/authorize"
#     r = requests.get(url=url, params=params)
#     return redirect(r.url)


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated " "successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def change_account(request):
    logout(request)
    return redirect("/social-auth/login/spotify/")


@login_required
def no_change(request):
    return render(request, "dashboard/dashboard.html", {"section": "dashboard"})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request, "account/user/list.html", {"section": "people", "users": users}
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request, "account/user/detail.html", {"section": "people", "user": user}
    )


@ajax_required
@require_POST
@login_required
def check_task(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})
