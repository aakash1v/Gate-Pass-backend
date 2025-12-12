from api import views
from django.urls import include, path


urlpatterns = [
    path("", views.home),
    path("leave-requests/", include("apps.leave.urls"))
]
