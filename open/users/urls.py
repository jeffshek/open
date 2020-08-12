from django.urls import path

from open.users.constants import UserResourceNames
from open.users.views import EmptyView, UserDetailsView, UserDeleteView

# i hate by default there's an app name here
app_name = "users"

urlpatterns = [
    # used by django for some random redirects, they always need this populate, so just put a blank view
    path("~redirect/", view=EmptyView.as_view(), name=UserResourceNames.USER_REDIRECT),
    path("details/", view=UserDetailsView.as_view(), name=UserResourceNames.DETAILS),
    # welp, this makes me sad, but i guess it's final then, so long and thanks for the fishes
    # not technically rest, but paranoia makes me create a separate endpoint
    path(
        "delete_user_confirmed/<uuid:uuid>/",
        view=UserDeleteView.as_view(),
        name=UserResourceNames.DELETE_USER_CONFIRMED,
    ),
]
