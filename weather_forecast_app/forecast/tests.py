from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import City
from .serializers import CitySerializers
from .utils import get_geo_location_by_name_city

PARAM_FOR_GET = {
    "name": "Penza",
    "latitude": 53.20066,
    "longitude": 45.00464,
}


class ForecastTestCase(TestCase):
    fixtures = [
        "weather_forecast_app/fixtures/db.json",
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_history_list(self) -> None:
        response = self.client.get(reverse("forecast:history_view"))
        response_cities_list = response.context["cities_list"]
        cities_list = (City.objects.filter(user_id=self.user.pk).
                       values("name", "latitude", "longitude").distinct().
                       order_by("name"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertQuerysetEqual(response_cities_list, cities_list)

    def test_history_list_not_auth(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("forecast:history_view"))
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertIn(str(settings.LOGIN_URL), response.url)

    def test_cites_list(self) -> None:
        response = self.client.post(reverse("forecast:city_form_view"), PARAM_FOR_GET)
        response_cities_list = response.context["cities_list"]
        res = get_geo_location_by_name_city(PARAM_FOR_GET.get("name"))
        self.assertEqual(response_cities_list, res)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cites_list_not_auth(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("forecast:city_form_view"))
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertIn(str(settings.LOGIN_URL), response.url)

    def test_forecast_near_future(self) -> None:
        response = self.client.get(reverse("forecast:forecast_near_future_view", kwargs=PARAM_FOR_GET))
        self.assertContains(response, PARAM_FOR_GET.get("name"))

    def test_forecast_near_future_not_auth(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("forecast:forecast_near_future_view", kwargs=PARAM_FOR_GET))
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertIn(str(settings.LOGIN_URL), response.url)

    def test_city_search_counter(self) -> None:
        _ = self.client.get(reverse("forecast:forecast_near_future_view", kwargs=PARAM_FOR_GET))
        after_request = City.objects.filter(name=PARAM_FOR_GET.get("name"))
        self.assertEqual(after_request[0].count, 1)


class CitiesViewSetTestCase(APITestCase):
    fixtures = [
        "weather_forecast_app/fixtures/db.json",
    ]

    def test_list(self):
        response = self.client.get(reverse("city_count_list-list"))
        queryset = City.objects.all().order_by("-count", "name")
        queryset_cities_list = [city.to_json() for city in queryset]
        serializers_data = CitySerializers(queryset, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertQuerysetEqual(queryset_cities_list, serializers_data)

    def test_pagination(self):
        response = self.client.get(reverse("city_count_list-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
