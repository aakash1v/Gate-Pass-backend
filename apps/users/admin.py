from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Staff


class StudentInline(admin.StackedInline):
    model = Student
    extra = 1

    # Hide inline if usertype is not student
    def has_view_or_change_permission(self, request, obj=None):
        if obj and obj.usertype == "student":
            return True
        return False

    def has_add_permission(self, request, obj):
        if obj and obj.usertype == "student":
            return True
        return False


class StaffInline(admin.StackedInline):
    model = Staff
    extra = 1

    # Hide inline if usertype is not staff
    def has_view_or_change_permission(self, request, obj=None):
        if obj and obj.usertype == "staff":
            return True
        return False

    def has_add_permission(self, request, obj):
        if obj and obj.usertype == "staff":
            return True
        return False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "usertype", "first_name", "last_name"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "dob", "mobile")}),
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

