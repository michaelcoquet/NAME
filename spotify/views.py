from django.shortcuts import render


def db_admin(request):
    return render(request, "spotify/db_admin.html", {"section": "db_admin"})
