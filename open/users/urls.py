from django.urls import path

from open.users.views import EmptyView, UserDetailsView

app_name = "users"

urlpatterns = [
    path("~redirect/", view=EmptyView.as_view(), name="redirect"),
    path("details/", view=UserDetailsView.as_view(), name="details"),
]
