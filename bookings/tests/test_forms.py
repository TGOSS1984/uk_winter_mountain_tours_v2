# bookings/tests/test_forms.py
from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth.models import User

from bookings.forms import BookingForm
from bookings.models import Guide, Route, Booking


class BookingFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.future_date = date.today() + timedelta(days=7)
        cls.guide_free = Guide.objects.create(name="Free Guide", email="free@example.com")
        cls.guide_taken = Guide.objects.create(name="Taken Guide", email="taken@example.com")
        cls.route = Route.objects.create(
            name="Mam Tor Ridge",
            region="peak_district",
            gpx_path="routes/mam_tor.gpx",
            distance_km=8.5,
            duration_hours=4,
        )

    def test_guest_must_provide_name_and_email(self):
        form = BookingForm(data={
            "route": self.route.id,
            "guide": self.guide_free.id,
            "date": self.future_date.isoformat(),
            "time_slot": "AM",
            # missing customer_name / customer_email
        })
        self.assertFalse(form.is_valid())
        self.assertIn("Provide customer_name and customer_email", str(form.errors))

    def test_logged_in_user_fields_hidden_not_required_and_user_attached(self):
        user = User.objects.create_user(username="alex", password="x")

        form = BookingForm(
            data={
                "route": self.route.id,
                "guide": self.guide_free.id,
                "date": self.future_date.isoformat(),
                "time_slot": "AM",
                # no customer_name/email on purpose
            },
            user=user,
        )

        # Fields are not required & hidden
        self.assertFalse(form.fields["customer_name"].required)
        self.assertFalse(form.fields["customer_email"].required)
        self.assertEqual(form.fields["customer_name"].widget.__class__.__name__, "HiddenInput")
        self.assertEqual(form.fields["customer_email"].widget.__class__.__name__, "HiddenInput")

        self.assertTrue(form.is_valid(), form.errors)
        booking = form.save(commit=False)
        self.assertEqual(booking.user, user)

    def test_duplicate_booking_same_guide_date_slot_invalid(self):
        # Occupy (guide_taken, future_date, AM)
        Booking.objects.create(
            guide=self.guide_taken,
            route=self.route,
            date=self.future_date,
            time_slot="AM",
            customer_name="Alice",
            customer_email="alice@example.com",
        )

        form = BookingForm(data={
            "route": self.route.id,
            "guide": self.guide_taken.id,
            "date": self.future_date.isoformat(),
            "time_slot": "AM",
            "customer_name": "Bob",
            "customer_email": "bob@example.com",
        })

        # __init__ filters guide queryset, so taken guide becomes an invalid choice
        self.assertFalse(form.is_valid())
        self.assertIn("Select a valid choice", str(form.errors))

        # extra assurance: taken guide is excluded from queryset
        qs_ids = set(form.fields["guide"].queryset.values_list("id", flat=True))
        self.assertNotIn(self.guide_taken.id, qs_ids)

    def test_guide_queryset_excludes_taken_guides_for_selected_slot(self):
        # Occupy (guide_taken, future_date, PM)
        Booking.objects.create(
            guide=self.guide_taken,
            route=self.route,
            date=self.future_date,
            time_slot="PM",
            customer_name="Alice",
            customer_email="alice@example.com",
        )

        form = BookingForm(data={
            "route": self.route.id,
            "guide": "",  # not selecting yet; inspecting queryset
            "date": self.future_date.isoformat(),
            "time_slot": "PM",
            "customer_name": "Chris",
            "customer_email": "chris@example.com",
        })

        qs_ids = set(form.fields["guide"].queryset.values_list("id", flat=True))
        self.assertIn(self.guide_free.id, qs_ids)
        self.assertNotIn(self.guide_taken.id, qs_ids)
