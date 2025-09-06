from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('equipment/', views.equipment, name='equipment'),
    path('gallery/', views.gallery, name='gallery'),
    path('regions/lake-district/', views.lake_district, name='lake_district'),
    path('regions/scotland/', views.scotland, name='scotland'),
    path('regions/wales/', views.wales, name='wales'),
    path('regions/peak-district/', views.peak_district, name='peak_district'),
]
