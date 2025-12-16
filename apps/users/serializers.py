from apps.core.models import Department, Hostel
from apps.users.models import Staff, Student
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    # Student fields
    prn = serializers.CharField(required=False)
    parents_name = serializers.CharField(required=False, allow_blank=True)
    parents_number = serializers.CharField(required=False, allow_blank=True)
    room_number = serializers.CharField(required=False, allow_blank=True)
    hostel_id = serializers.PrimaryKeyRelatedField(
        queryset=Hostel.objects.all(),
        required=False,
        allow_null=True
    )

    # Staff fields
    role = serializers.CharField(required=False)

    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "mobile",
            "dob",
            "usertype",

            # shared
            "department_id",

            # student
            "prn",
            "parents_name",
            "parents_number",
            "hostel_id",
            "room_number",

            # staff
            "role",
        )

    def validate(self, attrs):
        usertype = attrs.get("usertype")

        if usertype == "student":
            if not attrs.get("prn"):
                raise serializers.ValidationError(
                    {"prn": "PRN is required for students"}
                )

        if usertype == "staff":
            if not attrs.get("role"):
                raise serializers.ValidationError(
                    {"role": "Role is required for staff"}
                )

        if usertype == "admin":
            raise serializers.ValidationError(
                {"usertype": "Admin signup is not allowed"}
            )

        return attrs

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "This username is already taken."
            )
        return value
    
    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )
        return value

    def validate_prn(self, value):
        if Student.objects.filter(prn=value).exists():
            raise serializers.ValidationError(
                "A student with this PRN already exists."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        usertype = validated_data.pop("usertype")
        department = validated_data.pop("department_id")

        # Extract student fields
        prn = validated_data.pop("prn", None)
        parents_name = validated_data.pop("parents_name", "")
        parents_number = validated_data.pop("parents_number", "")
        hostel = validated_data.pop("hostel_id", None)
        room_number = validated_data.pop("room_number", "")

        # Extract staff fields
        role = validated_data.pop("role", None)

        password = validated_data.pop("password")

        user = User.objects.create(
            usertype=usertype,
            **validated_data
        )
        user.set_password(password)
        user.save()

        if usertype == "student":
            Student.objects.create(
                user=user,
                prn=prn,
                parents_name=parents_name,
                parents_number=parents_number,
                department=department,
                hostel=hostel,
                room_number=room_number,
            )

        elif usertype == "staff":
            Staff.objects.create(
                user=user,
                department=department,
                role=role,
                admin_approved=False,
            )

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
        try:
            s = obj.student_profile
            return {
                "prn": s.prn,
                "parents_name": s.parents_name,
                "parents_number": s.parents_number,
                "hostel": s.hostel.name,
                "room_number": s.room_number,
                "department": s.department.name,
            }
        except:
            return None

    def get_staff_profile(self, obj):
        try:
            s = obj.staff_profile
            return {
                "department": s.department.name,
                "role": s.role,
                "admin_approved": s.admin_approved,
            }
        except:
            return None
