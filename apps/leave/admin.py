from django.contrib import admin
from apps.leave.models import GatePass, LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "user", "starting_date", "final_status")
    list_filter = (
        "final_status",
        "approvedby_warden",
        "approvedby_hod",
        "approvedby_teacher",
    )
    search_fields = ("subject", "student__user__username", "user__student__prn")


@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "student",
        "get_leave_subject",
        "get_leave_status",
        "status",
        "issued_at",
    )

    list_filter = (
        "status",
        "leave_request__final_status",
    )

    search_fields = (
        "id",
        "student__prn",
        "student__user__username",
        "leave_request__subject",
    )

    readonly_fields = (
        "id",
        "code",
        "issued_at",
    )

    ordering = ("-issued_at",)

    def get_leave_subject(self, obj):
        return obj.leave_request.subject
    get_leave_subject.short_description = "Leave Subject"

    def get_leave_status(self, obj):
        return obj.leave_request.final_status
    get_leave_status.short_description = "Leave Status"
