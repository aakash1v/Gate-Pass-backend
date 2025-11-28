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
    branch = models.CharField(max_length=100)
    hostel = models.CharField(max_length=100)


class Staff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile"
    )
    department = models.CharField(max_length=100)
    role = models.CharField(
        max_length=20,
        choices=[
            ("teacher", "Teacher"),
            ("hod", "Head of Department"),
            ("warden", "Warden"),
            ("dean", "Principal"),
            ("other", "Other"),
        ]
    )
    admin_approved = models.BooleanField(default=False)
