from django.urls import path
from . import views


urlpatterns = [
    path("", views.LeaveRequestListCreateView.as_view()),
    path("my/", views.MyLeaveRequestListView.as_view()),
    path(
        "<int:pk>/approve/",
        views.LeaveApproveView.as_view(),
        name="leave-approve",
    ),
    path(
        "<int:pk>/reject/",
        views.LeaveRejectView.as_view(),
        name="leave-reject",
    ),
    path("gatepasses/", views.GatePassListAPIView.as_view(), name="gatepass-list"),
    path(
        "student/gate-passes/",
        views.StudentGatePassListAPIView.as_view(),
        name="student-gate-pass-list",
    ),


]
