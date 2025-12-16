from rest_framework import serializers
from .models import Department, Hostel


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "code",
            "is_active",
            "created_at",
        ]


class HostelSerializer(serializers.ModelSerializer):
    warden_name = serializers.SerializerMethodField()

    class Meta:
        model = Hostel
        fields = [
            "id",
            "name",
            "hostel_type",
            "total_capacity",
            "is_active",
            "warden",
            "warden_name",
            "created_at",
        ]

    def get_warden_name(self, obj):
        """
        Safely return full name of the warden if assigned.
        """
        if obj.warden and obj.warden.staff.user:
            return obj.warden.staff.user.get_full_name()
        return None

