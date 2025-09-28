from datetime import date
from django.test import TransactionTestCase, override_settings
from django.core import mail
from django.contrib.auth.models import User

from bookings.models import Booking, Guide, Route
from bookings.services import send_booking_email


@override_settings(
    ENABLE_EMAIL_NOTIFICATIONS=True,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="noreply@example.com",
)
class EmailTests(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice", email="alice@example.com", password="x"
        )
        # NOTE: use actual Route fields
        self.route = Route.objects.create(
            name="Test Route",
            region="wales",  # must be one of REGION_CHOICES keys
            gpx_path="routes/test.gpx",  # model uses gpx_path
            distance_km=1,  # DecimalField with int here
            duration_hours=1.0,  # or Decimal
        )
        self.guide = Guide.objects.create(name="Guide", email="g@example.com")

    def test_confirmation_email_sends(self):
        b = Booking.objects.create(
            user=self.user,
            route=self.route,
            guide=self.guide,
            date=date(2025, 12, 31),
            time_slot="AM",  # matches TIME_SLOTS
            status="confirmed",
        )
        send_booking_email(
            self.user,
            b,
            template_base="booking_confirmation",
            subject="Your booking is confirmed",
        )
        self.assertGreaterEqual(len(mail.outbox), 1)
        self.assertIn("confirmed", mail.outbox[-1].subject.lower())

    def test_cancellation_email_sends(self):
        b = Booking.objects.create(
            user=self.user,
            route=self.route,
            guide=self.guide,
            date=date(2025, 12, 31),
            time_slot="AM",
            status="cancelled",
        )
        send_booking_email(
            self.user,
            b,
            template_base="booking_cancellation",
            subject="Your booking has been cancelled",
        )
        self.assertGreaterEqual(len(mail.outbox), 1)
        self.assertIn("cancelled", mail.outbox[-1].subject.lower())
