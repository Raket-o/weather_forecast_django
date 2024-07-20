from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
from .models import City
from .forms import CityForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView

from .utils import get_forecast_weather, get_geo_location_by_name_city


@login_required
def forecast_near_future_view(request, **kwargs):
    latitude = round(float(kwargs.get("latitude")), 2)
    longitude = round(float(kwargs.get("longitude")), 2)
    name = kwargs.get("name")
    forecast_weather = get_forecast_weather(latitude, longitude)
    return render(request, template_name="forecast/forecast_near_future.html", context={"name": name, "forecast_weather": forecast_weather})


# class CitiesListView(ListView):
#     template_name = "forecast/cities_list.html"
#     queryset = (
#         City.objects
#         .all()
#     )


class CityFormView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return True

    model = City
    form_class = CityForm

    def form_valid(self, form) -> None:
        city = form.cleaned_data.get("name")
        cities_list = get_geo_location_by_name_city(city)

        form.instance.created_by = self.request.user
        form.save()
        return render(self.request, template_name="forecast/cities_list.html", context={"cities_list": cities_list})
