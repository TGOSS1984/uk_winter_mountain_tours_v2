from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

def index(request): return render(request,'pages/index.html')

def equipment(request): return render(request,'pages/equipment.html')

def gallery(request): return render(request,'pages/gallery.html')

def lake_district(request): return render(request,'pages/regions/lake_district.html')

def scotland(request): return render(request,'pages/regions/scotland.html')

def wales(request): return render(request,'pages/regions/wales.html')

def peak_district(request): return render(request,'pages/regions/peak_district.html')

class SignupView(CreateView):
    form_class=UserCreationForm
    template_name='registration/signup.html'
    success_url=reverse_lazy('login')
