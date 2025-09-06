from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from .models import Guide, Route, Booking
class BookingTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='alice', password='pass12345')
        self.guide=Guide.objects.create(name='Guide One', email='g1@example.com')
        self.route=Route.objects.create(name='Helvellyn via Striding Edge', region='lake_district', gpx_path='routes/lake_district/helvellyn.gpx')
        self.date=date.today()
    def test_prevent_double_booking(self):
        Booking.objects.create(user=self.user, route=self.route, guide=self.guide, date=self.date, time_slot='AM')
        with self.assertRaises(Exception):
            b2=Booking(user=self.user, route=self.route, guide=self.guide, date=self.date, time_slot='AM'); b2.full_clean()
    def test_booking_list_requires_login(self):
        resp=self.client.get(reverse('booking_list')); assert resp.status_code==302
        self.client.login(username='alice', password='pass12345')
        resp=self.client.get(reverse('booking_list')); assert resp.status_code==200
