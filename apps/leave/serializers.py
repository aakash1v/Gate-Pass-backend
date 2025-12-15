from rest_framework.serializers import ModelSerializer
from apps.leave.models import GatePass, LeaveRequest

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFlatSerializer(serializers.ModelSerializer):
    prn = serializers.SerializerMethodField()
    parents_name = serializers.SerializerMethodField()
    parents_number = serializers.SerializerMethodField()
    room_number = serializers.SerializerMethodField()
    hostel = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "prn",
            "parents_name",
            "parents_number",
            "hostel",
            "room_number",
            "department",
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
            return obj.student_profile.hostel.name
        return None

    def get_department(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.department.name
        return None

    def get_parents_name(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.parents_name
        return None

    def get_parents_number(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.parents_number
        return None

    def get_room_number(self, obj):
        if hasattr(obj, "student_profile"):
            return obj.student_profile.room_number
        return None


class LeaveRequestSerializer(ModelSerializer):
    user = UserFlatSerializer(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = "__all__"


class GatePassListSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    prn = serializers.CharField(source="student.prn", read_only=True)
    department = serializers.CharField(source="student.department.name", read_only=True)
    hostel = serializers.CharField(source="student.hostel.name", read_only=True)
    room_number = serializers.CharField(source="student.room_number", read_only=True)
    valid_from = serializers.DateTimeField(
        source="leave_request.starting_date", read_only=True
    )
    valid_until = serializers.DateTimeField(
        source="leave_request.ending_date", read_only=True
    )
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = GatePass
        fields = (
            "id",
            "code",
            "status",
            "issued_at",
            "valid_from",
            "valid_until",
            "is_valid",
            "student_name",
            "prn",
            "department",
            "hostel",
            "room_number",
        )

    def get_student_name(self, obj):
        user = obj.student.user
        return f"{user.first_name} {user.last_name}".strip()

    def get_is_valid(self, obj):
        return obj.is_valid()
