# bookings/views_routes.py
from django_filters.views import FilterView
from django.views.generic import ListView
from .models import Route
from .filters import RouteFilter


class AllRoutesView(FilterView, ListView):
    """
    All routes, filterable + paginated.
    """

    model = Route
    template_name = "pages/routes/all_routes.html"
    context_object_name = "routes"
    filterset_class = RouteFilter
    paginate_by = 9
    ordering = ["name"]  # keep deterministic order
