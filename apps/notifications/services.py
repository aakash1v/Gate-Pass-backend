from django.core.mail import send_mail
from django.conf import settings


def send_leave_status_email(user, leave_request):
    subject = f"Leave Request {leave_request.final_status}"
    message = f"""
Hello {user.first_name},

Your leave request "{leave_request.subject}" has been
{leave_request.final_status}.

From: {leave_request.starting_date}
To: {leave_request.ending_date}

Regards,
GatePass System
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
