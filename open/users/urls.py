from django.urls import path

from open.users.views import EmptyView

app_name = "users"

urlpatterns = [
    path("~redirect/", view=EmptyView.as_view(), name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
