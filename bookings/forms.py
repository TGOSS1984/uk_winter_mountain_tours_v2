# bookings/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, Guide

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['route', 'guide', 'date', 'time_slot', 'customer_name', 'customer_email']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # <-- keep your user-aware behaviour
        super().__init__(*args, **kwargs)

        # Hide customer fields for logged-in users (your original behaviour)
        if user and user.is_authenticated:
            self.fields['customer_name'].widget = forms.HiddenInput()
            self.fields['customer_email'].widget = forms.HiddenInput()

        # Default: all guides
        self.fields['guide'].queryset = Guide.objects.all()

        # If date & time are present (on POST/bound form), exclude already-booked guides
        data = self.data or {}
        date_val = data.get('date') or self.initial.get('date') or getattr(self.instance, 'date', None)
        time_val = data.get('time_slot') or self.initial.get('time_slot') or getattr(self.instance, 'time_slot', None)

        if date_val and time_val:
            taken_ids = (Booking.objects
                         .filter(date=date_val, time_slot=time_val)
                         .values_list('guide_id', flat=True))
            self.fields['guide'].queryset = Guide.objects.exclude(id__in=taken_ids)

    def clean(self):
        """
        Server-side safety net to prevent race conditions:
        if the selected guide/date/time is already taken, raise a validation error.
        (This works alongside your DB uniqueness constraint.)
        """
        cleaned = super().clean()
        guide = cleaned.get('guide')
        date = cleaned.get('date')
        time_slot = cleaned.get('time_slot')
        if guide and date and time_slot:
            conflict = Booking.objects.filter(guide=guide, date=date, time_slot=time_slot).exists()
            if conflict:
                raise ValidationError("That guide is already booked for the selected date and time.")
        return cleaned
