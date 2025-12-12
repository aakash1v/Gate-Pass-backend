from rest_framework import generics

from apps.leave.models import LeaveRequest
from apps.leave.serializers import LeaveRequestSerializer


class LeaveRequestListView(generics.ListCreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
