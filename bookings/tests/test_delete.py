from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings  # NEW import

from bookings.models import Booking, Route, Guide
from datetime import date

User = get_user_model()


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage",
    WHITENOISE_AUTOREFRESH=True,  # avoids hashed lookups in dev/test
)
class BookingDeleteTests(TestCase):
    def setUp(self):
        # Minimal related objects
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
            date=date.today(),
            time_slot="AM",
            status="confirmed",
        )

    def test_delete_booking_permanently_removes_record(self):
        self.client.login(username="u", password="p")
        url = reverse("booking_delete", args=[self.booking.pk])
        # confirm page GET
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)
        # submit POST to delete
        resp_post = self.client.post(url, follow=True)
        self.assertEqual(resp_post.status_code, 200)
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_delete_requires_login(self):
        url = reverse("booking_delete", args=[self.booking.pk])
        resp = self.client.post(url)
        # expect redirect to login
        self.assertIn(resp.status_code, (301, 302))

    def test_user_cannot_delete_someone_elses_booking(self):
        self.client.login(username="x", password="p")
        url = reverse("booking_delete", args=[self.booking.pk])
        resp = self.client.post(url, follow=True)
        # 404 because of ownership guard in get_object_or_404
        self.assertEqual(resp.status_code, 404)
        # still exists
        self.assertTrue(Booking.objects.filter(pk=self.booking.pk).exists())
