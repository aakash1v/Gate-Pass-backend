from api import views
from django.urls import include, path


urlpatterns = [
    path("", views.home),
    path("leave-request/", include("apps.leave.urls"))
]
