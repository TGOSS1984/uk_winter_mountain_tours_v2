from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from bookings.models import Booking, Route, Guide

User = get_user_model()


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    WHITENOISE_AUTOREFRESH=True,
)
class BookingUpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="p")
        self.other = User.objects.create_user(username="x", password="p")
        self.route = Route.objects.create(
            name="Test Route",
            region="lake_district",
            gpx_path="routes/helvellyn.gpx",
            distance_km=10,
            duration_hours=5,
            difficulty="moderate",
        )
        self.guide = Guide.objects.create(name="Guide A", email="guide@example.com")

        self.booking = Booking.objects.create(
            user=self.user,
            route=self.route,
            guide=self.guide,
            date=date.today() + timedelta(days=2),
            time_slot="AM",
            status="confirmed",
        )

    def test_owner_can_get_edit_page(self):
        self.client.login(username="u", password="p")
        url = reverse("booking_update", args=[self.booking.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Edit Booking")

    def test_owner_can_update_booking(self):
        self.client.login(username="u", password="p")
        url = reverse("booking_update", args=[self.booking.pk])
        new_date = date.today() + timedelta(days=5)
        resp = self.client.post(
            url,
            {
                "route": self.route.id,
                "guide": self.guide.id,
                "date": new_date,
                "time_slot": "PM",
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.date, new_date)
        self.assertEqual(self.booking.time_slot, "PM")

    def test_non_owner_gets_404(self):
        self.client.login(username="x", password="p")
        url = reverse("booking_update", args=[self.booking.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_past_date_is_rejected(self):
        self.client.login(username="u", password="p")
        url = reverse("booking_update", args=[self.booking.pk])
        resp = self.client.post(
            url,
            {
                "route": self.route.id,
                "guide": self.guide.id,
                "date": date.today() - timedelta(days=1),
                "time_slot": "AM",
            },
        )
        # Should re-render form (200) with errors
        self.assertEqual(resp.status_code, 200)
        self.booking.refresh_from_db()
        self.assertNotEqual(self.booking.date, date.today() - timedelta(days=1))
