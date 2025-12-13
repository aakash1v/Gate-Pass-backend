from django.db import models
from django.utils import timezone


class LeaveRequest(models.Model):
    TYPE_CHOICES = [
        ("Normal", "Normal"),
        ("Urgent", "Urgent"),
    ]
    FINAL_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="Normal",
    )
    final_status = models.CharField(
        max_length=20,
        choices=FINAL_STATUS_CHOICES,
        default="Pending",
    )

    subject = models.CharField(max_length=250)
    description = models.TextField()

    attachment = models.FileField(upload_to="leave_attachments/")

    approvedby_warden = models.BooleanField(default=False)
    approvedby_hod = models.BooleanField(default=False)
    approvedby_teacher = models.BooleanField(default=False)

    final_status = models.CharField(max_length=150, default="Pending")

    starting_date = models.DateTimeField(null=True, blank=True)
    ending_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    ## Storing approval time optional ..
    approvedby_teacher_at = models.DateTimeField(null=True, blank=True)
    approvedby_hod_at = models.DateTimeField(null=True, blank=True)
    approvedby_warden_at = models.DateTimeField(null=True, blank=True)

    rejected_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rejected_leaves",
    )

    rejected_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.user.username}"

    def update_final_status(self):
        if self.type == "Urgent":
            if any([
                self.approvedby_teacher,
                self.approvedby_hod,
                self.approvedby_warden,
            ]):
                self.final_status = "Approved"
        else:
            if all([
                self.approvedby_teacher,
                self.approvedby_hod,
                self.approvedby_warden,
            ]):
                self.final_status = "Approved"


class Leave(models.Model):
    leave_request = models.OneToOneField(
        LeaveRequest,
        on_delete=models.CASCADE,
        related_name="final_leave",
    )
    created_at = models.DateTimeField(default=timezone.now)

    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)

    def __str__(self):
        return f"Leave for {self.student} ({self.leave_request.subject})"
