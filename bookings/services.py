# bookings/services.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db import transaction

def send_booking_email(user, booking, template_base: str, subject: str):
    """
    Render and send booking emails (txt+html) post-transaction.
    Skips if notifications disabled or user has no email.
    """
    if not getattr(settings, "ENABLE_EMAIL_NOTIFICATIONS", True):
        return

    ctx = {"user": user, "booking": booking}
    txt = render_to_string(f"email/{template_base}.txt", ctx)
    html = render_to_string(f"email/{template_base}.html", ctx)

    def _send():
        if not (user and user.email):
            return
        msg = EmailMultiAlternatives(
            subject=subject,
            body=txt,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

    transaction.on_commit(_send)
