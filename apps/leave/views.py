from apps.notifications.services import send_leave_status_email
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone


from apps.leave.models import GatePass, LeaveRequest
from apps.leave.serializers import GatePassListSerializer, LeaveRequestSerializer

from rest_framework.pagination import PageNumberPagination


class StandardResultsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class LeaveRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        queryset = LeaveRequest.objects.all()

        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(final_status__iexact=status)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyLeaveRequestListView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class LeaveApproveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        leave = get_object_or_404(LeaveRequest, pk=pk)

        user = request.user
        now = timezone.now()

        # Only staff can approve
        if user.usertype != "staff":
            return Response(
                {"detail": "Only staff can approve leave requests"},
                status=status.HTTP_403_FORBIDDEN,
            )

        staff = user.staff_profile

        role = staff.role  # teacher / hod / warden
        if role == "teacher":
            if not leave.approvedby_teacher:
                leave.approvedby_teacher = True
                leave.approvedby_teacher_at = now

        elif role == "hod":
            if not leave.approvedby_hod:
                leave.approvedby_hod = True
                leave.approvedby_hod_at = now

        if role == "dean":
            if not leave.approvedby_dean:
                leave.approvedby_dean = True
                leave.approvedby_dean_at = now

        elif role == "warden":
            if not leave.approvedby_warden:
                leave.approvedby_warden = True
                leave.approvedby_warden_at = now

        elif role == "admin":
            if not leave.approvedby_admin:
                leave.approvedby_admin = True
                leave.approvedby_admin_at = now

        else:
            return Response(
                {"detail": "This role cannot approve leave"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 🔑 Apply business rules
        leave.update_final_status()
        leave.save()

        return Response(
            {
                "message": "Leave approved successfully",
                "final_status": leave.final_status,
            },
            status=status.HTTP_200_OK,
        )


class LeaveRejectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        leave = get_object_or_404(LeaveRequest, pk=pk)
        user = request.user

        # Only staff can reject
        if user.usertype != "staff":
            return Response(
                {"detail": "Only staff can reject leave requests"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Prevent double actions
        if leave.final_status == "Rejected":
            return Response(
                {"detail": "Leave request is already rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if leave.final_status == "Approved":
            return Response(
                {"detail": "Approved leave cannot be rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Perform rejection
        leave.final_status = "Rejected"
        leave.rejected_by = user
        leave.rejected_at = timezone.now()
        leave.rejection_reason = request.data.get("reason", "")

        leave.save()
        send_leave_status_email(leave.user, leave)

        return Response(
            {
                "message": "Leave request rejected successfully",
                "final_status": leave.final_status,
            },
            status=status.HTTP_200_OK,
        )


class GatePassListAPIView(generics.ListAPIView):
    serializer_class = GatePassListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        qs = GatePass.objects.select_related(
            "student",
            "student__user",
            "student__department",
            "student__hostel",
            "leave_request",
        ).order_by("-issued_at")

        # Optional filters
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs


class StudentGatePassListAPIView(generics.ListAPIView):
    serializer_class = GatePassListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        user = self.request.user

        # Safety check: ensure user is a student
        print(user)
        if not hasattr(user, "student_profile"):
            print("pass..")
            return GatePass.objects.none()

        qs = (
            GatePass.objects.select_related(
                "student",
                "student__user",
                "student__department",
                "student__hostel",
                "leave_request",
            )
            .filter(student=user.student_profile)
            .order_by("-issued_at")
        )

        # Optional filter
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)

        return qs

