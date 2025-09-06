from django.urls import path
from .views import BookingListView, BookingCreateView
urlpatterns=[ path('', BookingListView.as_view(), name='booking_list'), path('new/', BookingCreateView.as_view(), name='booking_create'), ]
