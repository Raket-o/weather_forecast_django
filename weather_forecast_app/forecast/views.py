from django.db.models import Count

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, View

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
        # latitude = round(float(kwargs.get("latitude")), 2)
        latitude = round(float(kwargs.get("latitude")), 0)
        # latitude = int(kwargs.get("latitude"), 0)
        # longitude = round(float(kwargs.get("longitude")), 2)
        longitude = round(float(kwargs.get("longitude")), 0)
        # longitude = int(kwargs.get("longitude"), 0)
        name = kwargs.get("name")
        print("+=-"*50, latitude, longitude)

        city_obj = City(
            name=name,
            latitude=latitude,
            longitude=longitude,
        )
        city_obj.save()
        current_user = User.objects.filter(id=self.request.user.pk)
        city_obj.user_id.set(current_user)
        forecast_weather = get_forecast_weather(latitude, longitude)

        name = str(name)
        # name = name.encode('utf-8')
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
    # queryset = City.objects.all()
    queryset = City.objects.all().values("name", "latitude", "longitude").annotate(count=Count("name", distinct=True)).order_by("-name")
    serializer_class = CitySerializers
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "name",
    ]
    filterset_fields = [
        "name",
    ]
    ordering_fields = [
        "name",
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


#     def

# class CityCountList(object):
#     def get_serializer(self, *args, **kwargs):
#         """ if an array is passed, set serializer to many """
#         if isinstance(kwargs.get('data', {}), list):
#             kwargs['many'] = True
#         return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)
#
#
# class CityCountList(CreateListModelMixin, generics.CreateAPIView):
#     serializer_class = CitySerializers


from rest_framework import generics
# # class CityCountList(generics.ListCreateAPIView):
# #     queryset = City.objects.all()
# #     serializer_class = CitySerializers
#
# class CityCountList(generics.ListCreateAPIView):
#     queryset = City.objects.all()
#     serializer_class = CitySerializers
#     # permission_classes = [IsAdminUser]
#
#     def list(self, request):
#         # Note the use of `get_queryset()` instead of `self.queryset`
#         queryset = self.get_queryset()
#         serializer = CitySerializers(queryset, many=True)
#         return Response(serializer.data)
