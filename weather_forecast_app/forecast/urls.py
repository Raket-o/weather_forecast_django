from django.urls import path

from .views import (
    # CitiesListView,
    cities_list_view,
    # CityCreateView,
    request_city_from_user

#     AdvertisingCompaniesListView,
#     AdvertisingCompanyCreateView,
#     AdvertisingCompanyDeleteView,
#     AdvertisingCompanyDetailsView,
#     AdvertisingCompanyUpdateView,
#     AdvertisingCompanyViewSet,
)

app_name = "forecast"

urlpatterns = [
    # path("", CitiesListView.as_view(), name="cities_list_view"),
    # path("", CityCreateView.as_view(), name="city_create_view"),
    path("", request_city_from_user, name="request_city_from_user"),
    # path("<str:name>/", cities_list_view, name="cities_list_view"),
    path("cities/", cities_list_view, name="cities_list_view"),

    # path("", AdvertisingCompaniesListView.as_view(), name="advertising_companies_list"),
#     path("create/", AdvertisingCompanyCreateView.as_view(), name="advertising_company_create"),
#     path("<int:pk>/", AdvertisingCompanyDetailsView.as_view(), name="advertising_company_details"),
#     path("<int:pk>/update/", AdvertisingCompanyUpdateView.as_view(), name="advertising_company_update"),
#     path("<int:pk>/delete/", AdvertisingCompanyDeleteView.as_view(), name="advertising_company_archived"),
]
