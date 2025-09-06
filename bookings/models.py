from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
class Guide(models.Model):
    name=models.CharField(max_length=100); email=models.EmailField()
    phone=models.CharField(max_length=30, blank=True); bio=models.TextField(blank=True)
    def __str__(self): return self.name
REGION_CHOICES=[('lake_district','Lake District'),('scotland','Scotland'),('wales','Wales'),('peak_district','Peak District')]
class Route(models.Model):
    name=models.CharField(max_length=150)
    region=models.CharField(max_length=30, choices=REGION_CHOICES)
    gpx_path=models.CharField(max_length=255, help_text="Relative path to GPX under /routes")
    distance_km=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    duration_hours=models.DecimalField(max_digits=4, decimal_places=1, default=0)
    def __str__(self): return f"{self.name} ({self.get_region_display()})"
TIME_SLOTS=[('AM','Morning (8:00–12:00)'),('PM','Afternoon (13:00–17:00)')]
STATUS_CHOICES=[('confirmed','Confirmed'),('cancelled','Cancelled')]
class Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name=models.CharField(max_length=120, blank=True)
    customer_email=models.EmailField(blank=True)
    route=models.ForeignKey(Route, on_delete=models.CASCADE)
    guide=models.ForeignKey(Guide, on_delete=models.CASCADE)
    date=models.DateField()
    time_slot=models.CharField(max_length=2, choices=TIME_SLOTS, default='AM')
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['guide','date','time_slot'], name='unique_guide_timeslot')]
    def clean(self):
        if not self.user and (not self.customer_name or not self.customer_email):
            raise ValidationError("Provide customer_name and customer_email when not logged in.")
        if Booking.objects.exclude(pk=self.pk).filter(guide=self.guide, date=self.date, time_slot=self.time_slot, status='confirmed').exists():
            raise ValidationError("Selected guide is already booked for this date/time slot.")
    def get_absolute_url(self): return reverse('booking_list')
    def __str__(self): return f"{self.route} with {self.guide} on {self.date} ({self.time_slot})"
