from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView, View

from .models import City
from .forms import CityForm
from .utils import get_forecast_weather, get_geo_location_by_name_city


class ForecastNearFutureView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return True

    def get(self, request, **kwargs):
        latitude = round(float(kwargs.get("latitude")), 2)
        longitude = round(float(kwargs.get("longitude")), 2)
        name = kwargs.get("name")
        city_obj = City(
            name=name,
            latitude=latitude,
            longitude=longitude,
        )
        city_obj.save()
        current_user = User.objects.filter(id=self.request.user.pk)
        city_obj.user_id.set(current_user)
        forecast_weather = get_forecast_weather(latitude, longitude)
        return render(request, template_name="forecast/forecast_near_future.html",
                      context={"name": name, "forecast_weather": forecast_weather})


class ForecastNearFutureView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return True

    def get(self, request, **kwargs):
        latitude = round(float(kwargs.get("latitude")), 2)
        longitude = round(float(kwargs.get("longitude")), 2)
        name = kwargs.get("name")
        city_obj = City(
            name=name,
            latitude=latitude,
            longitude=longitude,
        )
        city_obj.save()
        current_user = User.objects.filter(id=self.request.user.pk)
        city_obj.user_id.set(current_user)
        forecast_weather = get_forecast_weather(latitude, longitude)
        return render(request, template_name="forecast/forecast_near_future.html",
                      context={"name": name, "forecast_weather": forecast_weather})



#
# @login_required
# def forecast_near_future_view(request, **kwargs):
#     print(kwargs)
#     latitude = round(float(kwargs.get("latitude")), 2)
#     longitude = round(float(kwargs.get("longitude")), 2)
#     name = kwargs.get("name")
#     user_pk = kwargs.get("user_pk")
#     city_obj = City(
#         name=name,
#         latitude= latitude,
#         longitude= longitude,
#     )
#     # city_obj.save()
#     # city_obj.pk
#     # current_user = User(city_obj)
#     # current_user.save()
#     print(type(user_pk), user_pk)
#     current_user = User.objects.filter(id=user_pk)
#     print("+="*30)
#
#     # print(current_user.__dict__)
#     # print("+="*30, current_user.__dict__)
#
#
#     forecast_weather = get_forecast_weather(latitude, longitude)
#     return render(request, template_name="forecast/forecast_near_future.html", context={"name": name, "forecast_weather": forecast_weather})
#
#
# # class CitiesListView(ListView):
# #     template_name = "forecast/cities_list.html"
# #     queryset = (
# #         City.objects
# #         .all()
# #     )


class CityFormView(UserPassesTestMixin, CreateView):
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return True

    model = City
    form_class = CityForm

    def form_valid(self, form):
        city = form.cleaned_data.get("name")
        cities_list = get_geo_location_by_name_city(city)

        form.instance.created_by = self.request.user
        # form.save()
        # print("+="*30, self.request.user)
        # print("+="*30, self.request.user.pk)
        # user_pk = self.request.user.pk
        # queryset = User.objects.filter(id=user_pk)
        # print("form_valid+=" * 30, queryset)
        return render(
            self.request,
            template_name="forecast/cities_list.html",
            context={"cities_list": cities_list}
        )
