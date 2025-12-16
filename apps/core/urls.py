from django.urls import path
from .views import DepartmentListAPIView, HostelListAPIView

urlpatterns = [
    path("departments/", DepartmentListAPIView.as_view(), name="department-list"),
    path("hostels/", HostelListAPIView.as_view(), name="hostel-list"),
]
