from django.urls import path
from .views import BookingListView, BookingCreateView, cancel_booking

urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'),
    path('new/', BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>/cancel/', cancel_booking, name='booking_cancel'),
]
