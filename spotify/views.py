from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


# @user_passes_test(lambda u: u.is_superuser)
def db_admin(request):
    if request.user.is_superuser:
        return render(request, "spotify/db_admin.html", {"section": "db_admin"})
    else:
        return render(
            request, "spotify/db_admin_login.html", {"section": "db_admin_login"}
        )
