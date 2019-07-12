from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

urlpatterns = [
    path(
        "",
        default_views.permission_denied,
        kwargs={"exception": Exception("Shame On You")},
        name="unnamed",
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    path("writeup/v1/", include("open.core.writeup.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
