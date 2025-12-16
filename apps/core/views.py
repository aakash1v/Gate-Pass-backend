from rest_framework import generics, permissions
from .models import Department, Hostel
from .serializers import DepartmentSerializer, HostelSerializer


class DepartmentListAPIView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Department.objects.filter(is_active=True)


class HostelListAPIView(generics.ListAPIView):
    serializer_class = HostelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Hostel.objects.filter(is_active=True)

        hostel_type = self.request.query_params.get("type")
        if hostel_type:
            qs = qs.filter(hostel_type=hostel_type)

        return qs

