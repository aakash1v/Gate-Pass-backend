from api import views
from apps.users.views import MeView, UserListView
from django.urls import include, path


urlpatterns = [
    path("", views.home),
    path("leave-requests/", include("apps.leave.urls")),
    path("core/", include("apps.core.urls")),
    path("users/", UserListView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),

]
