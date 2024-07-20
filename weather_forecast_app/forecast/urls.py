from django.urls import path

from .views import (
    CityFormView,
    forecast_near_future_view,
)


app_name = "forecast"

urlpatterns = [
    path("", CityFormView.as_view(), name="city_form_view"),
    path("cities/name=<str:name>&lat=<str:latitude>&lon=<str:longitude>/", forecast_near_future_view, name="forecast_near_future_view"),
]
