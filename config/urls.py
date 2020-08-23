from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import RedirectView

from open.users.views import (
    GitHubLogin,
    LoginNoCSRFAPIView,
    RegisterNoCSRFAPIView,
)

# need a special view to make sure favicon always works
favicon_view = RedirectView.as_view(
    url="/static/images/favicons/gatsby-icon.png", permanent=True
)


def trigger_error(request):
    division_by_zero = 1 / 0
    return division_by_zero


urlpatterns = [
    path("sentry-debug/", trigger_error),
    path(
        "",
        default_views.permission_denied,
        kwargs={"exception": Exception("Shame On You")},
        name="unnamed",
    ),
    path("rest-auth/login/", LoginNoCSRFAPIView.as_view(), name="rest_login"),
    # TODO - reconsider how registration should work with writeup.ai
    path(
        "rest-auth/registration/",
        RegisterNoCSRFAPIView.as_view(),
        name="rest_registration",
    ),
    re_path(
        r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        RedirectView.as_view(
            url=f"{settings.BETTERSELF_APP_URL}/password_reset/%(uidb64)s/%(token)s/"
        ),
        name="password_reset_confirm",
    ),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("rest-auth/github/", GitHubLogin.as_view(), name="github_login"),
    path("favicon.ico", favicon_view, name="favicon"),
    path(settings.ADMIN_URL, admin.site.urls),
    # prefix an api endpoint in front of everything to use a global load balancer
    # and route traffic based on API variants. this is to offload websocket servers
    # and traditional REST servers
    path("api/writeup/v1/", include("open.core.writeup.urls")),
    path("api/betterself/v2/", include("open.core.betterself.urls")),
    path("users/", include("open.users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
