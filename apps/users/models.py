from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Django already has: first_name, last_name, email, username, password
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    usertype = models.CharField(
        max_length=20,
        choices=[("student", "Student"), ("staff", "Staff"), ("admin", "Admin")],
        default="student",
    )

    def __str__(self):
        return self.username


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    prn = models.CharField(max_length=20, unique=True)
    parents_name = models.CharField(max_length=250, null=True, blank=True)
    parents_number = models.CharField(max_length=250, null=True, blank=True)

    department = models.ForeignKey(
        "core.Department",
        on_delete=models.PROTECT,
        related_name="students"
    )
    hostel = models.ForeignKey(
        "core.Hostel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    def __str__(self):
        return f"{self.user.username} ({self.prn})"


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile"
    )
    department = models.ForeignKey(
        "core.Department",   # string reference = safest
        on_delete=models.PROTECT,
        related_name="staff_members"
    )
    role = models.CharField(
        max_length=20,
        choices=[
            ("teacher", "Teacher"),
            ("hod", "HOD"),
            ("warden", "Warden"),
            ("dean", "Dean"),
            ("other", "Other"),
        ],
    )
    admin_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}({self.role})"


class WardenProfile(models.Model):
    staff = models.OneToOneField(
        Staff, on_delete=models.CASCADE, related_name="warden_profile"
    )

    office_phone = models.CharField(max_length=15)
    office_location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Warden: {self.staff.user.username}"
