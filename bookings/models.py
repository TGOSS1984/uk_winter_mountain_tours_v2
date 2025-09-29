from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.db.models import OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.text import slugify
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles import finders


class Guide(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


REGION_CHOICES = [
    ("lake_district", "Lake District"),
    ("scotland", "Scotland"),
    ("wales", "Wales"),
    ("peak_district", "Peak District"),
]

DIFFICULTY_CHOICES = [
    ("easy", "Easy"),
    ("moderate", "Moderate"),
    ("hard", "Hard"),
    ("severe", "Severe"),
]


class Route(models.Model):
    name = models.CharField(max_length=150)
    region = models.CharField(max_length=30, choices=REGION_CHOICES)
    gpx_path = models.CharField(
        max_length=255, help_text="Relative path to GPX under /routes"
    )
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    duration_hours = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        blank=True,
        null=True,
        help_text="Overall route difficulty",
    )

    def __str__(self):
        return f"{self.name} ({self.get_region_display()})"

    @property
    def image_url(self) -> str:
        """
        1) slug-based image (webp/jpg/png)
        2) region fallback (webp)
        3) global placeholder
        Works in dev (finders) and prod (storage).
        """

        def exists(rel_path: str) -> bool:
            return bool(finders.find(rel_path) or staticfiles_storage.exists(rel_path))

        slug = slugify(self.name or "")
        candidates = [
            f"images/routes/{slug}.webp",
            f"images/routes/{slug}.jpg",
            f"images/routes/{slug}.png",
        ]
        for rel in candidates:
            if exists(rel):
                return static(rel)

        region_key = slugify(self.get_region_display() or "")
        if region_key:
            region_rel = f"images/routes/fallbacks/{region_key}.webp"
            if exists(region_rel):
                return static(region_rel)

        return static("images/hero/ben-nevis-scenic-hero.webp")


TIME_SLOTS = [("AM", "Morning (8:00–12:00)"), ("PM", "Afternoon (13:00–17:00)")]
STATUS_CHOICES = [("confirmed", "Confirmed"), ("cancelled", "Cancelled")]


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=120, blank=True)
    customer_email = models.EmailField(blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=2, choices=TIME_SLOTS, default="AM")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="confirmed"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["guide", "date", "time_slot"], name="unique_guide_timeslot"
            )
        ]

    def clean(self):
        # Guest path: require name+email when no authenticated user is attached
        if not self.user_id and (not self.customer_name or not self.customer_email):
            raise ValidationError(
                "Provide customer_name and customer_email when not logged in."
            )

        # Only check conflicts when all keys are present; use *_id to avoid dereferencing unset FKs
        if self.guide_id and self.date and self.time_slot:
            conflict = (
                Booking.objects.exclude(pk=self.pk)
                .filter(
                    guide_id=self.guide_id,
                    date=self.date,
                    time_slot=self.time_slot,
                    status="confirmed",
                )
                .exists()
            )
            if conflict:
                raise ValidationError(
                    "Selected guide is already booked for this date/time slot."
                )

    def get_absolute_url(self):
        return reverse("booking_list")

    def __str__(self):
        return f"{self.route} with {self.guide} on {self.date} ({self.time_slot})"


# --- addition for Profiles ---


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
