from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import Booking
from .forms import BookingForm

@method_decorator(login_required, name='dispatch')
class BookingListView(ListView):
    template_name='bookings/booking_list.html'
    context_object_name='bookings'
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-date','-created_at')

@method_decorator(login_required, name='dispatch')
class BookingCreateView(CreateView):
    template_name='bookings/booking_form.html'
    form_class=BookingForm
    success_url=reverse_lazy('booking_list')
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs(); kwargs['user']=self.request.user; return kwargs
    def form_valid(self, form):
        booking=form.save(commit=False); booking.user=self.request.user
        try:
            booking.full_clean(); booking.save(); messages.success(self.request,'Booking created successfully.')
            return redirect(self.success_url)
        except Exception as e:
            form.add_error(None, e); return self.form_invalid(form)
