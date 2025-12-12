from rest_framework.serializers import ModelSerializer
from apps.leave.models import LeaveRequest


class LeaveRequestSerializer(ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = "__all__"
