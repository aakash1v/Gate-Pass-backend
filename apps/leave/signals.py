from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.leave.models import GatePass, LeaveRequest


@receiver(post_save, sender=LeaveRequest)
def create_gatepass_on_approval(sender, instance, created, **kwargs):
    """
    Automatically create GatePass when LeaveRequest is approved.
    """

    # Only act when leave is approved
    if not instance.is_approved():
        return

    # Prevent duplicate gatepasses
    if hasattr(instance, "gatepass"):
        return

    # Safety: dates must exist
    if not instance.starting_date or not instance.ending_date:
        return

    GatePass.objects.create(
        leave_request=instance,
        student=instance.user.student_profile,  # assuming OneToOne User → Student
        issued_by=None,  # optional: set system user later
    )
