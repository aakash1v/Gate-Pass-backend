from django.urls import path
from . import views


urlpatterns = [
    path("", views.LeaveRequestListView.as_view()),
    path("my/", views.MyLeaveRequestListView.as_view()),
]
