# bookings/tests/test_views.py
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from bookings.models import Guide, Route, Booking


class BookingCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.future_date = date.today() + timedelta(days=7)
        cls.user = User.objects.create_user(username="testuser", password="secret")
        cls.guide = Guide.objects.create(name="Guide One", email="guide@example.com")
        cls.route = Route.objects.create(
            name="Helvellyn",
            region="lake_district",
            gpx_path="routes/helvellyn.gpx",
            distance_km=10,
            duration_hours=5,
        )

    def test_get_booking_form_authenticated(self):
        self.client.login(username="testuser", password="secret")
        url = reverse("booking_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name=\"route\"")  # basic form field check
        self.assertContains(response, "name=\"guide\"")

    def test_post_valid_booking_creates_record(self):
        self.client.login(username="testuser", password="secret")
        url = reverse("booking_create")
        data = {
            "route": self.route.id,
            "guide": self.guide.id,
            "date": self.future_date.isoformat(),
            "time_slot": "AM",
            # name/email not required since user is authenticated
        }
        response = self.client.post(url, data, follow=True)
        # Redirect to booking_list
        self.assertRedirects(response, reverse("booking_list"))
        # One booking exists
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.route, self.route)
        self.assertEqual(booking.guide, self.guide)
