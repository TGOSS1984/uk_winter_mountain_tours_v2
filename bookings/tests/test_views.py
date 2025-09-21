# bookings/tests/test_views.py
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

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

class CancelBookingViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser2", password="secret")
        cls.guide = Guide.objects.create(name="Guide Two", email="guide2@example.com")
        cls.route = Route.objects.create(
            name="Scafell Pike",
            region="lake_district",
            gpx_path="routes/scafell.gpx",
            distance_km=12,
            duration_hours=6,
        )
        cls.future_date = timezone.now().date() + timedelta(days=5)

    def setUp(self):
        self.client.login(username="testuser2", password="secret")
        self.booking = Booking.objects.create(
            user=self.user,
            guide=self.guide,
            route=self.route,
            date=self.future_date,
            time_slot="AM",
        )

    def test_post_cancels_future_booking(self):
        url = reverse("booking_cancel", args=[self.booking.pk])
        response = self.client.post(url, follow=True)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "cancelled")
        self.assertContains(response, "Booking cancelled.")

    def test_get_does_not_cancel_booking(self):
        url = reverse("booking_cancel", args=[self.booking.pk])
        response = self.client.get(url, follow=True)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")  # unchanged
        self.assertContains(response, "Invalid request method.")


class CancelPastBookingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="tester_past", password="secret")
        cls.guide = Guide.objects.create(name="Guide P", email="p@example.com")
        cls.route = Route.objects.create(
            name="Great Gable",
            region="lake_district",
            gpx_path="routes/great_gable.gpx",
            distance_km=11,
            duration_hours=6,
        )
        cls.past_date = timezone.now().date() - timedelta(days=2)

    def setUp(self):
        self.client.login(username="tester_past", password="secret")
        self.booking = Booking.objects.create(
            user=self.user,
            guide=self.guide,
            route=self.route,
            date=self.past_date,  # in the past
            time_slot="AM",
        )

    def test_post_cannot_cancel_past_booking(self):
        url = reverse("booking_cancel", args=[self.booking.pk])
        resp = self.client.post(url, follow=True)
        self.booking.refresh_from_db()

        # Status should remain confirmed
        self.assertEqual(self.booking.status, "confirmed")
        # Error flash shown
        self.assertContains(resp, "Past bookings can’t be cancelled.")


class BookingListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_a = User.objects.create_user(username="alice", password="x")
        cls.user_b = User.objects.create_user(username="bob", password="x")
        guide = Guide.objects.create(name="Guide L", email="l@example.com")
        route = Route.objects.create(
            name="Blencathra",
            region="lake_district",
            gpx_path="routes/blencathra.gpx",
            distance_km=9,
            duration_hours=4,
        )
        d = timezone.now().date() + timedelta(days=3)
        # One booking for each user
        Booking.objects.create(user=cls.user_a, guide=guide, route=route, date=d, time_slot="AM")
        Booking.objects.create(user=cls.user_b, guide=guide, route=route, date=d, time_slot="PM")

    def test_list_shows_only_logged_in_users_bookings(self):
        self.client.login(username="alice", password="x")
        resp = self.client.get(reverse("booking_list"))
        self.assertEqual(resp.status_code, 200)
        bookings = list(resp.context["bookings"])
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0].user.username, "alice")

    def test_list_redirects_anonymous_to_login(self):
        resp = self.client.get(reverse("booking_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp.url)  # default auth login path


class BookingCreateInvalidPostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="invalid_poster", password="secret")
        cls.guide = Guide.objects.create(name="Guide Z", email="z@example.com")
        cls.route = Route.objects.create(
            name="Pillar",
            region="lake_district",
            gpx_path="routes/pillar.gpx",
            distance_km=10,
            duration_hours=5,
        )
        cls.future_date = date.today() + timedelta(days=10)

    def test_invalid_post_rerenders_form_with_errors_and_creates_nothing(self):
        self.client.login(username="invalid_poster", password="secret")
        url = reverse("booking_create")

        # Missing required fields (e.g., no route) + invalid guide id ensures validation fails
        data = {
            # "route": self.route.id,          # omit route to trigger error
            "guide": 999999,                    # not in queryset -> invalid choice
            "date": self.future_date.isoformat(),
            "time_slot": "AM",
        }

        resp = self.client.post(url, data)
        # Form should be re-rendered (no redirect)
        self.assertEqual(resp.status_code, 200)
        # Should show some error content
        self.assertContains(resp, "error", status_code=200)  # generic check
        # And no booking created
        self.assertEqual(Booking.objects.count(), 0)

