from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Staff


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    extra = 1


class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
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

    def get_inlines(self, request, obj=None):
        # If editing existing user
        if obj:
            if obj.usertype == "student":
                return [StudentInline]
            elif obj.usertype == "staff":
                return [StaffInline]
            return []

        # If adding a new user (obj is None)
        usertype = request.POST.get("usertype")

        if usertype == "student":
            return [StudentInline]
        elif usertype == "staff":
            return [StaffInline]

        return []

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inlines(request, obj):
            yield inline(self.model, self.admin_site)
