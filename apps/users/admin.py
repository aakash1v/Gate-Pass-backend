from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Staff, WardenProfile


class StudentInline(admin.StackedInline):
    model = Student
    extra = 1


class StaffInline(admin.StackedInline):
    model = Staff
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "usertype", "first_name", "last_name"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "dob", "mobile")},
        ),
        ("Role", {"fields": ("usertype",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "usertype",
                ),
            },
        ),
    )

    # Inlines always included — Django handles visibility
    inlines = [StudentInline, StaffInline]


@admin.register(WardenProfile)
class WardenProfileAdmin(admin.ModelAdmin):
    list_display = (
        "get_username",
        "get_department",
        "office_phone",
        "office_location",
    )

    search_fields = (
        "staff__user__username",
        "staff__user__first_name",
        "staff__user__last_name",
    )

    def get_username(self, obj):
        return obj.staff.user.username

    get_username.short_description = "Username"

    def get_department(self, obj):
        return obj.staff.department

    get_department.short_description = "Department"
