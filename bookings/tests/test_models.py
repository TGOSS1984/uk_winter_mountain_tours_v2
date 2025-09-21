from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import timedelta, date

from django.contrib.auth.models import User
from bookings.models import Guide, Route, Booking


class BookingModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guide = Guide.objects.create(
            name="Test Guide",
            email="guide@example.com",
            phone="07000000000",
            bio="Experienced guide",
        )
        cls.route = Route.objects.create(
            name="Mam Tor Ridge",
            region="peak_district",
            gpx_path="routes/mam_tor.gpx",
            distance_km=8.5,
            duration_hours=4,
        )
        cls.booking_date = date.today() + timedelta(days=7)

    def test_prevent_double_booking_same_guide_same_date_slot(self):
        """Booking.clean() and DB constraint should prevent double booking for same guide/date/slot."""
        Booking.objects.create(
            guide=self.guide,
            route=self.route,
            date=self.booking_date,
            time_slot="AM",
            customer_name="Alice",
            customer_email="alice@example.com",
        )

        duplicate = Booking(
            guide=self.guide,
            route=self.route,
            date=self.booking_date,
            time_slot="AM",
            customer_name="Bob",
            customer_email="bob@example.com",
        )

        # App-level validation or DB constraint should catch it
        with self.assertRaises((ValidationError, IntegrityError)):
            duplicate.full_clean()
            duplicate.save()

    def test_requires_customer_details_if_no_user(self):
        """If no user is linked, customer_name and customer_email must be provided."""
        booking = Booking(
            guide=self.guide,
            route=self.route,
            date=self.booking_date,
            time_slot="PM",
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_allows_booking_if_user_present_without_customer_fields(self):
        """A logged-in user can book without explicitly giving customer_name/email."""
        user = User.objects.create_user(username="testuser", password="secret")
        booking = Booking(
            user=user,
            guide=self.guide,
            route=self.route,
            date=self.booking_date,
            time_slot="PM",
        )
        # Should not raise
        booking.full_clean()
        booking.save()
        self.assertEqual(Booking.objects.count(), 1)

    def test_str_representation_is_informative(self):
        booking = Booking.objects.create(
            guide=self.guide,
            route=self.route,
            date=self.booking_date,
            time_slot="AM",
            customer_name="Alice",
            customer_email="alice@example.com",
        )
        text = str(booking)
        self.assertIn("Mam Tor Ridge", text)
        self.assertIn("Test Guide", text)
        self.assertIn("AM", text)
