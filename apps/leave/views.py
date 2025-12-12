from rest_framework import generics, permissions

from apps.leave.models import LeaveRequest
from apps.leave.serializers import LeaveRequestSerializer


class LeaveRequestListView(generics.ListCreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer


class MyLeaveRequestListView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
