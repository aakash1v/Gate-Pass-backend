from django.db import models
from django.utils import timezone
import uuid

from apps.notifications.services import send_leave_status_email
from apps.notifications.background import send_email_async
from .utils import generate_gatepass_code


class LeaveRequest(models.Model):
    TYPE_CHOICES = [
        ("Normal", "Normal"),
        ("Holiday", "Holiday"),
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
    approvedby_dean = models.BooleanField(default=False)
    approvedby_admin = models.BooleanField(default=False)

    starting_date = models.DateTimeField(null=True, blank=True)
    ending_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    ## Storing approval time optional ..
    approvedby_teacher_at = models.DateTimeField(null=True, blank=True)
    approvedby_hod_at = models.DateTimeField(null=True, blank=True)
    approvedby_warden_at = models.DateTimeField(null=True, blank=True)
    approvedby_dean_at = models.DateTimeField(null=True, blank=True)
    approvedby_admin_at = models.DateTimeField(null=True, blank=True)

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

    def should_be_approved(self):
        if self.type == "Holiday":
            return self.approvedby_warden

        admin_approved = any(
            [
                self.approvedby_dean,
                self.approvedby_hod,
                self.approvedby_admin,
            ]
        )

        return self.approvedby_warden and admin_approved

    def update_final_status(self):
        if self.is_rejected():
            return

        if self.should_be_approved():
            self.final_status = "Approved"
            self.save(update_fields=["final_status"])
            send_email_async(send_leave_status_email(self.user, self))

    def is_approved(self):
        return self.final_status == "Approved"

    def is_rejected(self):
        return self.final_status == "Rejected"


class GatePass(models.Model):
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Used", "Used"),
        ("Expired", "Expired"),
        ("Revoked", "Revoked"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        editable=False,
    )

    leave_request = models.OneToOneField(
        LeaveRequest,
        on_delete=models.CASCADE,
        related_name="gatepass",
    )

    student = models.ForeignKey(
        "users.Student",
        on_delete=models.CASCADE,
        related_name="gatepasses",
    )

    issued_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active",
    )

    issued_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_gatepasses",
    )

    def valid_from(self):
        return self.leave_request.starting_date

    def valid_until(self):
        return self.leave_request.ending_date

    def is_valid(self):
        now = timezone.now()

        if self.status != "Active":
            return False

        if not self.leave_request.is_approved():
            return False

        if not self.valid_from() or not self.valid_until():
            return False

        return self.valid_from() <= now <= self.valid_until()

    def refresh_status(self):
        now = timezone.now()

        if self.status == "Active" and now > self.valid_until():
            self.status = "Expired"
            self.save(update_fields=["status"])

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = generate_gatepass_code()
                if not GatePass.objects.filter(code=code).exists():
                    self.code = code
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"GatePass {self.id} - {self.student}"
