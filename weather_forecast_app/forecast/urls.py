from django.urls import path
from .views import (
    CityFormView,
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
]
