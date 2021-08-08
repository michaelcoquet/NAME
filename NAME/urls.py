from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from account.views import social_auth_complete

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("account/", include("account.urls")),
    # path(
    #     "social-auth/complete/spotify/",
    #     social_auth_complete,
    #     name="social_complete",
    # ),
    path("social-auth/", include("social_django.urls", namespace="social")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("account/", include("account.urls")),
#     path("social-auth/", include("social_django.urls", namespace="social")),
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
