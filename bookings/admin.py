from django.contrib import admin
from .models import Guide, Route, Booking
@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin): list_display=('name','email','phone')
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin): list_display=('name','region','distance_km','duration_hours')
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=('route','guide','date','time_slot','user','status')
    list_filter=('date','time_slot','status','guide','route')
    search_fields=('user__username','customer_name','customer_email')
