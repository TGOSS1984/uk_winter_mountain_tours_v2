from django.urls import path

from . import views

from bookings.views_routes import AllRoutesView

urlpatterns = [
    path("", views.index, name="index"),
    path("equipment/", views.equipment, name="equipment"),
    path("gallery/", views.gallery, name="gallery"),
    path("regions/lake-district/", views.lake_district, name="lake_district"),
    path("regions/scotland/", views.scotland, name="scotland"),
    path("regions/wales/", views.wales, name="wales"),
    path("regions/peak-district/", views.peak_district, name="peak_district"),
    path("about/", views.about, name="about"),
    path("routes/", AllRoutesView.as_view(), name="routes_all"),
]
