from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.index_template = "admin/index.html"
admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("db/", include("spotify.urls")),
    path("", include("dashboard.urls")),
    path("account/", include("account.urls")),
    path("social-auth/", include("social_django.urls", namespace="social")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
