import pytest
from django.urls import reverse
from bookings.models import Route


@pytest.mark.django_db
def test_all_routes_page_renders(client):
    Route.objects.create(
        name="Short Easy",
        region="wales",
        gpx_path="routes/a.gpx",
        distance_km=5,
        duration_hours=2,
        difficulty="easy",
    )
    Route.objects.create(
        name="Long Hard",
        region="scotland",
        gpx_path="routes/b.gpx",
        distance_km=20,
        duration_hours=10,
        difficulty="severe",
    )

    url = reverse("routes_all")
    resp = client.get(url)
    assert resp.status_code == 200
    assert b"All Routes" in resp.content


@pytest.mark.django_db
def test_filter_by_region_and_difficulty(client):
    Route.objects.create(
        name="A",
        region="wales",
        gpx_path="routes/a.gpx",
        distance_km=6,
        duration_hours=3,
        difficulty="easy",
    )
    Route.objects.create(
        name="B",
        region="scotland",
        gpx_path="routes/b.gpx",
        distance_km=12,
        duration_hours=6,
        difficulty="severe",
    )

    resp = client.get(reverse("routes_all"), {"region": "wales", "difficulty": "easy"})
    assert resp.status_code == 200

    routes = resp.context["routes"]  # set by context_object_name in the view
    names = {r.name for r in routes}
    assert "A" in names
    assert "B" not in names
    assert len(routes) == 1


@pytest.mark.django_db
def test_filter_distance_duration_ranges(client):
    Route.objects.create(
        name="Med Route",
        region="wales",
        gpx_path="routes/a.gpx",
        distance_km=10,
        duration_hours=4,
        difficulty="moderate",
    )
    Route.objects.create(
        name="Far Route",
        region="wales",
        gpx_path="routes/b.gpx",
        distance_km=30,
        duration_hours=12,
        difficulty="hard",
    )

    url = reverse("routes_all")
    resp = client.get(
        url, {"distance_min": "8", "distance_max": "12", "duration_max": "5"}
    )
    content = resp.content.decode()
    assert "Med Route" in content
    assert "Far Route" not in content
