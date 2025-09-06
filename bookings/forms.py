# bookings/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Booking, Guide


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['route', 'guide', 'date', 'time_slot', 'customer_name', 'customer_email']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'customer_email': forms.EmailInput(attrs={'type': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        # Keep your user-aware behaviour, but also bind it to the instance
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            # ✅ Critical: attach user BEFORE validation so model.clean() sees it
            self.instance.user = user

            # Logged-in users don't need to fill these
            self.fields['customer_name'].required = False
            self.fields['customer_email'].required = False
            self.fields['customer_name'].widget = forms.HiddenInput()
            self.fields['customer_email'].widget = forms.HiddenInput()

        # Default: all guides
        self.fields['guide'].queryset = Guide.objects.all()

        # If date & time are present (on POST/bound form), exclude already-booked guides
        data = self.data or {}
        date_val = data.get('date') or self.initial.get('date') or getattr(self.instance, 'date', None)
        time_val = data.get('time_slot') or self.initial.get('time_slot') or getattr(self.instance, 'time_slot', None)

        if date_val and time_val:
            taken_ids = (
                Booking.objects
                .filter(date=date_val, time_slot=time_val)
                .values_list('guide_id', flat=True)
            )
            self.fields['guide'].queryset = Guide.objects.exclude(id__in=list(taken_ids))

    def clean(self):
        """
        - If anonymous, require customer_name & customer_email (friendly error).
        - Double-booking guard (alongside your DB unique constraint).
        """
        cleaned = super().clean()

        user = getattr(self.instance, 'user', None)
        if not (user and getattr(user, 'is_authenticated', False)):
            name = cleaned.get('customer_name')
            email = cleaned.get('customer_email')
            if not name or not email:
                raise ValidationError("Provide customer_name and customer_email when not logged in.")

        guide = cleaned.get('guide')
        date = cleaned.get('date')
        time_slot = cleaned.get('time_slot')
        if guide and date and time_slot:
            conflict = Booking.objects.filter(guide=guide, date=date, time_slot=time_slot).exists()
            if conflict:
                raise ValidationError("That guide is already booked for the selected date and time.")

        return cleaned

