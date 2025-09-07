# core/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from django.utils.text import slugify
from bookings.models import Route


def _route_ids_for(region_code: str) -> dict:
    """
    Build {slugified_name: id} for routes in a given region.
    Slug uses hyphens -> then we replace with underscores so it's template-friendly.
    """
    routes = Route.objects.filter(region=region_code).only('id', 'name')
    return {slugify(r.name).replace('-', '_'): r.id for r in routes}


def index(request):
    return render(request, 'pages/index.html')

def equipment(request):
    return render(request, 'pages/equipment.html')

def gallery(request):
    return render(request, 'pages/gallery.html')

def lake_district(request):
    ctx = {'route_ids': _route_ids_for('lake_district')}
    return render(request, 'pages/regions/lake_district.html', ctx)

def scotland(request):
    ctx = {'route_ids': _route_ids_for('scotland')}
    return render(request, 'pages/regions/scotland.html', ctx)

def wales(request):
    ctx = {'route_ids': _route_ids_for('wales')}
    return render(request, 'pages/regions/wales.html', ctx)

def peak_district(request):
    ctx = {'route_ids': _route_ids_for('peak_district')}
    return render(request, 'pages/regions/peak_district.html', ctx)

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
