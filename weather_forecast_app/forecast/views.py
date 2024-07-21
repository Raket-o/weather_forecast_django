from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.models import User
from django.views.generic import CreateView, View

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import City
from .forms import CityForm
from .serializers import CitySerializers
from .utils import get_forecast_weather, get_geo_location_by_name_city


class ForecastNearFutureView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return True

    def get(self, request, **kwargs):
        latitude = round(float(kwargs.get("latitude")), 0)
        longitude = round(float(kwargs.get("longitude")), 0)
        name = kwargs.get("name")

        city_obj = City.objects.filter(name=name)
        try:
            city_obj = city_obj[0]
        except IndexError:
            pass

        if city_obj:
            city_obj.count += 1

        else:
            city_obj = City(
                name=name,
                latitude=latitude,
                longitude=longitude,
                count=1,
            )

        city_obj.save()

        user_current = User.objects.filter(id=self.request.user.pk)
        city_obj.user_id.set(user_current)
        forecast_weather = get_forecast_weather(latitude, longitude)

        return render(request, template_name="forecast/forecast_near_future.html",
                      context={"name": name, "forecast_weather": forecast_weather})


class HistoryView(UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            return True

    def get(self, request):
        cities_list = (City.objects.filter(user_id=self.request.user.pk).
                       values("name", "latitude", "longitude").distinct().
                       order_by("name"))
        return render(
            request,
            template_name="forecast/history_list.html",
            context={"cities_list": cities_list}
        )


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
        return render(
            self.request,
            template_name="forecast/cities_list.html",
            context={"cities_list": cities_list}
        )


class CityCountList(ModelViewSet):
    queryset = City.objects.all().order_by("-count", "name")
    serializer_class = CitySerializers
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "name",
        "count"
    ]
    filterset_fields = [
        "name",
        "count"
    ]
    ordering_fields = [
        "name",
        "count"
    ]

    def create(self, request, *args, **kwargs):
        return Response({'error': 'The method is not available'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        return Response({'error': 'The method is not available'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        return Response({'error': 'The method is not available'}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        return Response({'error': 'The method is not available'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'The method is not available'}, status=status.HTTP_403_FORBIDDEN)
