from django.urls import path

from .views import BookingCreateView, BookingListView, cancel_booking
from .views import booking_delete  # Added for full CRUD functionality - true delete

from django.views.generic import TemplateView

urlpatterns = [
    path("", BookingListView.as_view(), name="booking_list"),
    path("new/", BookingCreateView.as_view(), name="booking_create"),
    path("<int:pk>/cancel/", cancel_booking, name="booking_cancel"),
    # new hard delete end point added
    path("<int:pk>/delete/", booking_delete, name="booking_delete"),
    path(
        "thank-you/contact/",
        TemplateView.as_view(template_name="thankyou/contact.html"),
        name="thank_you_contact",
    ),
    path(
        "thank-you/hello/",
        TemplateView.as_view(template_name="thankyou/hello.html"),
        name="thank_you_hello",
    ),
    path(
        "thank-you/subscribe/",
        TemplateView.as_view(template_name="thankyou/subscribe.html"),
        name="thank_you_subscribe",
    ),
]
