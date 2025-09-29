# bookings/filters.py
import django_filters as filters
from .models import Route


class RouteFilter(filters.FilterSet):
    distance_min = filters.NumberFilter(
        field_name="distance_km", lookup_expr="gte", label="Min distance (km)"
    )
    distance_max = filters.NumberFilter(
        field_name="distance_km", lookup_expr="lte", label="Max distance (km)"
    )
    duration_min = filters.NumberFilter(
        field_name="duration_hours", lookup_expr="gte", label="Min duration (h)"
    )
    duration_max = filters.NumberFilter(
        field_name="duration_hours", lookup_expr="lte", label="Max duration (h)"
    )

    class Meta:
        model = Route
        fields = ["region", "difficulty"]  # choices come from model
