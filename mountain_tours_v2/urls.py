from django.contrib import admin
from django.urls import path, include
from core.views import SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('bookings/', include('bookings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignupView.as_view(), name='signup'),
]
