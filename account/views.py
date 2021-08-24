from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def user_login(request):
    return render(request, "registration/login.html")


@login_required
def change_account(request):
    logout(request)
    return redirect("/social-auth/login/spotify/")


@login_required
def no_change(request):
    return render(request, "dashboard/dashboard.html", {"section": "dashboard"})
