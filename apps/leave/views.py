from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils import timezone


from apps.leave.models import LeaveRequest
from apps.leave.serializers import LeaveRequestSerializer


class LeaveRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        print(role)
        if role == "teacher":
            if not leave.approvedby_teacher:
                leave.approvedby_teacher = True
                leave.approvedby_teacher_at = now

        elif role == "hod":
            if not leave.approvedby_hod:
                leave.approvedby_hod = True
                leave.approvedby_hod_at = now

        elif role == "warden":
            if not leave.approvedby_warden:
                leave.approvedby_warden = True
                leave.approvedby_warden_at = now

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

        return Response(
            {
                "message": "Leave request rejected successfully",
                "final_status": leave.final_status,
            },
            status=status.HTTP_200_OK,
        )
