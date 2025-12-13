from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import FullUserSerializer, SignupSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, Staff, User
from rest_framework.permissions import IsAuthenticated, AllowAny


def home(req):
    return JsonResponse({"msg": "Welcome to Gate Pass Backend !!"})


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

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
    permission_classes = [AllowAny]

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
                    "usertype": user.usertype,
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


class UserListView(ListAPIView):
    serializer_class = FullUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all().order_by("id")

        usertype = self.request.query_params.get("usertype")

        if usertype in ["student", "staff", "admin"]:
            queryset = queryset.filter(usertype=usertype)

        return queryset


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = FullUserSerializer(request.user)
        return Response(serializer.data)
