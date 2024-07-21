from django.urls import path

from forecast.models import City
from forecast.serializers import CitySerializers
from rest_framework.generics import ListCreateAPIView

from .views import (
    CityFormView,
    # forecast_near_future_view,
    ForecastNearFutureView,
    HistoryView,
)


app_name = "forecast"

urlpatterns = [
    path("", CityFormView.as_view(), name="city_form_view"),
    path("history/", HistoryView.as_view(), name="history_view"),
    path(
        "cities/name=<str:name>&lat=<str:latitude>&lon=<str:longitude>/",
        ForecastNearFutureView.as_view(), name="forecast_near_future_view"
    ),

    # path(
    #     'api/cities',
    #     ListCreateAPIView.as_view(
    #         queryset=City.objects.all(),
    #         serializer_class=CitySerializers
    #     ),
    #     name='count_cities'
    # )

]
