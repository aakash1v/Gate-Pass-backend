from django.urls import path
from . import views


urlpatterns = [
    path("all/", views.LeaveRequestListView.as_view()),
]
