from django.contrib import admin
from django.urls import include, path
from core.views import SignupView
from django.contrib.auth.views import LoginView
from core.forms import LoginForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("bookings/", include("bookings.urls")),
    # Put the custom login BEFORE the auth include so it takes precedence
    path(
        "accounts/login/",
        LoginView.as_view(authentication_form=LoginForm),
        name="login",
    ),
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # logout, password reset, etc.
    path("signup/", SignupView.as_view(), name="signup"),
]
