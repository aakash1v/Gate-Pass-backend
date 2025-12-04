from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "dob",
            "mobile",
            "usertype",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data["username"].strip()
        password = data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        data["user"] = user
        return data


class FullUserSerializer(serializers.ModelSerializer):
    student_profile = serializers.SerializerMethodField()
    staff_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "dob",
            "mobile",
            "usertype",
            "student_profile",
            "staff_profile",
        ]

    def get_student_profile(self, obj):
        if hasattr(obj, "student_profile"):
            s = obj.student_profile
            return {
                "prn": s.prn,
                "branch": s.branch,
                "hostel": s.hostel,
            }
        return None

    def get_staff_profile(self, obj):
        if hasattr(obj, "staff_profile"):
            s = obj.staff_profile
            return {
                "department": s.department,
                "role": s.role,
                "admin_approved": s.admin_approved,
            }
        return None
