from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Staff


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
