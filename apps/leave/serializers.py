from rest_framework.serializers import ModelSerializer
from apps.leave.models import LeaveRequest

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFlatSerializer(serializers.ModelSerializer):
    prn = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    parents_name = serializers.SerializerMethodField()
    parents_number = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "prn",
            "branch",
            "hostel",
            "parents_name",
            "parents_number",
        )

    def get_prn(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.prn
        return None

    def get_branch(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.branch
        return None

    def get_hostel(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.hostel
        return None

    def get_parents_name(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.parents_name
        return None

    def get_parents_number(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.parents_number
        return None


class LeaveRequestSerializer(ModelSerializer):
    user = UserFlatSerializer(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = "__all__"
