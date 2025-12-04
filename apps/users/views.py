from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import SignupSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, Staff


def home(req):
    return JsonResponse({"msg": "Welcome to Gate Pass Backend !!"})


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create user
        user = serializer.save()
        usertype = serializer.validated_data.get("usertype", "student")

        # Create profile depending on role
        if usertype == "student":
            Student.objects.create(
                user=user,
                prn=serializer.validated_data.get("prn", ""),
                branch=serializer.validated_data.get("branch", ""),
                hostel=serializer.validated_data.get("hostel", ""),
            )
        elif usertype == "staff":
            Staff.objects.create(
                user=user,
                department=serializer.validated_data.get("department", ""),
                role=serializer.validated_data.get("role", "other"),
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "usertype": user.usertype,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Remove Django's session login — not used with JWT
        # login(request, user)  <-- ❌ REMOVE THIS

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_200_OK,
        )
