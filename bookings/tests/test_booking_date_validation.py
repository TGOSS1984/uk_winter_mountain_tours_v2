import pytest
from django.utils import timezone
from bookings.forms import BookingForm
from bookings.models import Route, Guide


@pytest.mark.django_db
def test_booking_form_rejects_past_date():
    # Arrange: minimal related objects
    route = Route.objects.create(
        name="Test Route",
        region="lake_district",
        gpx_path="routes/lake_district/test.gpx",
        distance_km=10,
        duration_hours=4.0,
        difficulty="moderate",
    )
    guide = Guide.objects.create(
        name="Test Guide",
        email="guide@example.com",
        phone="+44 0000 000000",
        bio="Bio",
    )

    yesterday = timezone.localdate() - timezone.timedelta(days=1)

    # Act
    form = BookingForm(
        data={
            "route": route.id,
            "guide": guide.id,
            "date": yesterday,  # date object is fine
            "time_slot": "AM",
            "customer_name": "Test User",
            "customer_email": "test@example.com",
        }
    )

    # Assert
    assert not form.is_valid()
    assert "date" in form.errors
    assert "past" in form.errors["date"][0].lower()  # helpful message check


@pytest.mark.django_db
def test_booking_form_allows_today():
    # Arrange
    route = Route.objects.create(
        name="Test Route 2",
        region="wales",
        gpx_path="routes/wales/test.gpx",
        distance_km=8,
        duration_hours=3.0,
        difficulty="easy",
    )
    guide = Guide.objects.create(
        name="Another Guide",
        email="guide2@example.com",
        phone="+44 1111 111111",
        bio="Bio",
    )

    today = timezone.localdate()

    # Act
    form = BookingForm(
        data={
            "route": route.id,
            "guide": guide.id,
            "date": today,
            "time_slot": "AM",  # adjust if needed
            "customer_name": "Test User",
            "customer_email": "test@example.com",
        }
    )

    # Assert
    assert form.is_valid(), form.errors
