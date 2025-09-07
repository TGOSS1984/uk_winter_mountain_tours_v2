# bookings/views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now

from .models import Booking, Route  # <-- add Route here
from .forms import BookingForm


@method_decorator(login_required, name='dispatch')
class BookingListView(ListView):
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-date', '-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['today'] = now().date()  # for template checks like "future bookings"
        return ctx


@method_decorator(login_required, name='dispatch')
class BookingCreateView(CreateView):
    template_name = 'bookings/booking_form.html'
    form_class = BookingForm
    success_url = reverse_lazy('booking_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # NEW: preselect route from ?route_id=123 (best) or ?route=helvellyn-striding-edge (fallback)
    def get_initial(self):
        initial = super().get_initial()

        # Prefer an explicit numeric ID
        route_id = self.request.GET.get('route_id')
        if route_id and route_id.isdigit():
            try:
                initial['route'] = Route.objects.get(pk=route_id)
                return initial
            except Route.DoesNotExist:
                pass

        # Fallback: a slug-ish name like "helvellyn-striding-edge"
        route_slug = self.request.GET.get('route')
        if route_slug:
            name_guess = route_slug.replace('-', ' ').replace('_', ' ').strip()
            r = Route.objects.filter(name__iexact=name_guess).first()
            if not r:
                # last resort: partial match
                r = Route.objects.filter(name__icontains=name_guess).first()
            if r:
                initial['route'] = r

        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'booking_url': reverse_lazy('booking_create'),
            'hero_title': 'Explore the Mountains',
            'hero_subtitle': "Experience unforgettable tours across the UK's stunning snowy peaks",
            # paths are relative to STATIC and used by {% static hero_img %} inside the include
            'hero_img': 'images/hero/maincribgoch2048x1737px.webp',
            'hero_img_xl': 'images/hero/maincribgoch2048x1737px.webp',
        })
        return ctx

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        try:
            booking.full_clean()
            booking.save()
            messages.success(self.request, 'Booking created successfully.')
            return redirect(self.success_url)
        except Exception as e:
            form.add_error(None, e)
            return self.form_invalid(form)


@login_required
def cancel_booking(request, pk):
    """
    POST-only: cancel the user's own future booking.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('booking_list')

    if booking.date < now().date():
        messages.error(request, "Past bookings can’t be cancelled.")
        return redirect('booking_list')

    # Try to use enum value if your model defines Booking.Status.CANCELLED; otherwise fallback.
    cancel_value = getattr(getattr(Booking, 'Status', None), 'CANCELLED', None) or 'cancelled'
    booking.status = cancel_value
    booking.save(update_fields=['status'])
    messages.success(request, 'Booking cancelled.')
    return redirect('booking_list')

