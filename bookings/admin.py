# bookings/admin.py
from django.contrib import admin
from .models import Guide, Route, Booking

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_active_safe")
    search_fields = ("name", "email")

    def is_active_safe(self, obj):
        # Some versions of the model may not have is_active; default to True
        return getattr(obj, "is_active", True)
    is_active_safe.short_description = "active"
    is_active_safe.boolean = True


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "region_safe",
        "difficulty_safe",
        "distance_km_safe",
        "duration_hours_safe",
        "is_active_safe",
    )
    search_fields = ("name",)

    # Use helper accessors so missing fields don't crash admin
    def region_safe(self, obj):
        return getattr(obj, "region", "-")
    region_safe.short_description = "region"

    def difficulty_safe(self, obj):
        return getattr(obj, "difficulty", "-")
    difficulty_safe.short_description = "difficulty"

    def distance_km_safe(self, obj):
        # support either distance_km or distance
        val = getattr(obj, "distance_km", None)
        if val is None:
            val = getattr(obj, "distance", None)
        return val if val is not None else "-"
    distance_km_safe.short_description = "distance (km)"

    def duration_hours_safe(self, obj):
        val = getattr(obj, "duration_hours", None)
        if val is None:
            val = getattr(obj, "duration", None)
        return val if val is not None else "-"
    duration_hours_safe.short_description = "duration (hrs)"

    def is_active_safe(self, obj):
        return getattr(obj, "is_active", True)
    is_active_safe.short_description = "active"
    is_active_safe.boolean = True


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "route",
        "guide",
        "date_safe",
        "time_safe",
        "num_people_safe",
        "status_safe",
        "user",
    )
    # Keep search_fields to stable relations only
    search_fields = ("user__username", "route__name", "guide__name")

    def date_safe(self, obj):
        return getattr(obj, "date", getattr(obj, "start_date", "-"))
    date_safe.short_description = "date"

    def time_safe(self, obj):
        # Prefer start/end time if present, else fall back to time_slot if present
        st = getattr(obj, "start_time", None)
        et = getattr(obj, "end_time", None)
        if st and et:
            return f"{st}–{et}"
        ts = getattr(obj, "time_slot", None)
        return ts if ts else "-"
    time_safe.short_description = "time"

    def num_people_safe(self, obj):
        return getattr(obj, "num_people", getattr(obj, "party_size", "-"))
    num_people_safe.short_description = "people"

    def status_safe(self, obj):
        return getattr(obj, "status", "-")
    status_safe.short_description = "status"
