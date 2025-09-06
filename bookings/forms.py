from django import forms
from .models import Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        fields=['route','guide','date','time_slot','customer_name','customer_email']
        widgets={'date': forms.DateInput(attrs={'type':'date'})}
    def __init__(self,*args,**kwargs):
        user=kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user and user.is_authenticated:
            self.fields['customer_name'].widget=forms.HiddenInput()
            self.fields['customer_email'].widget=forms.HiddenInput()
