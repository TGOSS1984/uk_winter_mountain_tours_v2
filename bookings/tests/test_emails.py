from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth.models import User
from bookings.models import Booking, Guide, Route
from bookings.services import send_booking_email

@override_settings(
    ENABLE_EMAIL_NOTIFICATIONS=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@example.com",
)
class EmailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", "alice@example.com", "x")
        self.route = Route.objects.create(name="Test Route", region="wales", gpx_url="", distance_km=1, ascent_m=100, duration_hours=1)
        self.guide = Guide.objects.create(name="Guide", email="g@example.com")

    def test_confirmation_email_sends(self):
        b = Booking.objects.create(user=self.user, route=self.route, guide=self.guide, date="2025-12-31", time_slot="AM", status="confirmed")
        send_booking_email(self.user, b, "booking_confirmation", "Your booking is confirmed")
        self.assertTrue(mail.outbox)
        self.assertIn("confirmed", mail.outbox[-1].subject.lower())
