from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def start_scrape(request):
    request.user.profile.scrape_in_progress = True
    request.user.profile.save()
    return render(request, "spotify/scraping.html")


def db_admin(request):
    if request.user.is_superuser:
        if request.user.profile.scrape_in_progress == True:
            return render(request, "spotify/scraping.html")
        else:
            return render(request, "spotify/db_admin.html")
    else:
        return render(request, "spotify/db_admin_login.html")
