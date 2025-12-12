from django.contrib import admin
from apps.leave.models import Leave, LeaveRequest


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


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "leave_request", "created_at")

