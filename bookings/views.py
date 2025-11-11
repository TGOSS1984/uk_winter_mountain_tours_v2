# bookings/views.py
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import CreateView, ListView

from .forms import BookingForm, BookingUpdateForm
from .models import Booking, Route  # <-- add Route here
from .services import send_booking_email


@method_decorator(login_required, name="dispatch")
class BookingListView(ListView):
    template_name = "bookings/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by(
            "-date", "-created_at"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["today"] = now().date()  # for template checks like "future bookings"
        return ctx


@method_decorator(login_required, name="dispatch")
class BookingCreateView(CreateView):
    template_name = "bookings/booking_form.html"
    form_class = BookingForm
    success_url = reverse_lazy("booking_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    # NEW: preselect route from ?route_id=123 (best) or ?route=helvellyn-striding-edge (fallback)
    def get_initial(self):
        initial = super().get_initial()

        # Prefer an explicit numeric ID
        route_id = self.request.GET.get("route_id")
        if route_id and route_id.isdigit():
            try:
                initial["route"] = Route.objects.get(pk=route_id)
                return initial
            except Route.DoesNotExist:
                pass

        # Fallback: a slug-ish name like "helvellyn-striding-edge"
        route_slug = self.request.GET.get("route")
        if route_slug:
            name_guess = route_slug.replace("-", " ").replace("_", " ").strip()
            r = Route.objects.filter(name__iexact=name_guess).first()
            if not r:
                # last resort: partial match
                r = Route.objects.filter(name__icontains=name_guess).first()
            if r:
                initial["route"] = r

        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "booking_url": reverse_lazy("booking_create"),
                "hero_title": "Explore the Mountains",
                "hero_subtitle": "Experience unforgettable tours across the UK's stunning snowy peaks",
                # paths are relative to STATIC and used by {% static hero_img %} inside the include
                "hero_img": "images/hero/maincribgoch2048x1737px.webp",
                "hero_img_xl": "images/hero/maincribgoch2048x1737px.webp",
            }
        )
        return ctx

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        try:
            booking.full_clean()
            booking.save()
            send_booking_email(
                self.request.user,
                booking,
                template_base="booking_confirmation",
                subject="Your booking is confirmed",
            )
            messages.success(self.request, "Booking created successfully.")
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

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("booking_list")

    if booking.date < now().date():
        messages.error(request, "Past bookings can’t be cancelled.")
        return redirect("booking_list")

    # Try to use enum , otherwise fallback.
    cancel_value = (
        getattr(getattr(Booking, "Status", None), "CANCELLED", None) or "cancelled"
    )
    booking.status = cancel_value
    booking.save(update_fields=["status"])
    send_booking_email(
        request.user,
        booking,
        template_base="booking_cancellation",
        subject="Your booking has been cancelled",
    )
    messages.success(request, "Booking cancelled.")
    return redirect("booking_list")


# NEW: true delete
@login_required
def booking_delete(request, pk):
    """
    GET: show a confirmation page.
    POST: permanently delete the user's own booking (hard delete).
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == "POST":
        # HARD DELETE: remove the row from the database
        booking.delete()
        messages.success(request, "Booking deleted permanently.")
        return redirect("booking_list")

    return render(request, "bookings/booking_confirm_delete.html", {"booking": booking})


# NEW: Update booking
@login_required
def booking_update(request, pk):
    """Allow a user to edit their own booking."""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == "POST":
        form = BookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect("booking_list")
    else:
        form = BookingUpdateForm(instance=booking)

    return render(
        request,
        "bookings/booking_form_update.html",
        {"form": form, "booking": booking},
    )


def newsletter_subscribe(request):
    if request.method != "POST":
        # If someone visits directly, just send them to the thank-you page
        return redirect("thank_you_subscribe")

    email = (request.POST.get("email") or "").strip()
    try:
        validate_email(email)
        # TODO: optionally save email or send confirmation email here
        return redirect("thank_you_subscribe")
    except ValidationError:
        # Re-render the page or show an error template
        return render(
            request, "subscribe_error.html", {"error": "Invalid email address"}
        )
