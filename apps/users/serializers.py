from apps.users.models import Staff, Student
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # Student fields
    prn = serializers.CharField(required=False, allow_blank=True)
    parents_name = serializers.CharField(required=False, allow_blank=True)
    parents_number = serializers.CharField(required=False, allow_blank=True)

    # Staff fields
    role = serializers.CharField(required=False, allow_blank=True)

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

            # student profile
            "prn",
            "parents_name",
            "parents_number",

            # staff profile
            "role",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        # student fields
        prn = validated_data.pop("prn", None)
        parents_name = validated_data.pop("parents_name", None)
        parents_number = validated_data.pop("parents_number", None)

        # staff fields
        role = validated_data.pop("role", "other")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if user.usertype == "student":
            Student.objects.create(
                user=user,
                prn=prn,
                parents_name=parents_name,
                parents_number=parents_number,
            )

        elif user.usertype == "staff":
            Staff.objects.create(
                user=user,
                role=role.lower(),
            )

        return user

    def validate(self, data):
        usertype = data.get("usertype")

        if usertype == "student":
            prn = data.get("prn")

            if not prn:
                raise serializers.ValidationError(
                    {"prn": "PRN is required for student signup"}
                )

            if Student.objects.filter(prn=prn).exists():
                raise serializers.ValidationError(
                    {"prn": "A student with this PRN already exists"}
                )

        return data


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
        try:
            s = obj.student_profile
            return {
                "prn": s.prn,
                "parents_name": s.parents_name,
                "parents_number": s.parents_number,
            }
        except:
            return None

    def get_staff_profile(self, obj):
        try:
            s = obj.staff_profile
            return {
                # "department": s.department,
                "role": s.role,
                "admin_approved": s.admin_approved,
            }
        except:
            return None
