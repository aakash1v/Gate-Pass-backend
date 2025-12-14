from apps.core.models import Department, Hostel
from django.contrib import admin

admin.site.register(Department)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("name", "hostel_type", "total_capacity", "is_active")
    list_filter = ("hostel_type", "is_active")
