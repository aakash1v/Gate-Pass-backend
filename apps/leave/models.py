from django.db import models
from django.utils import timezone


class LeaveRequest(models.Model):
    type = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    description = models.TextField()

    parents_name = models.CharField(max_length=250)
    parents_number = models.CharField(max_length=20)
    attachment = models.FileField(upload_to="media/")

    approvedby_warden = models.BooleanField(default=False)
    approvedby_hod = models.BooleanField(default=False)
    approvedby_teacher = models.BooleanField(default=False)

    final_status = models.CharField(max_length=150, default="Pending")

    starting_date = models.DateTimeField(null=True, blank=True)
    ending_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.student}"


class Leave(models.Model):
    leave_request = models.OneToOneField(LeaveRequest, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)

    def __str__(self):
        return f"Leave for {self.student} ({self.leave_request.subject})"
