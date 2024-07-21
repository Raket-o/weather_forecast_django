from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

DATA = {
    "username": "test_user",
    "password1": "qsxcft234tgbk7",
    "password2": "qsxcft234tgbk7",
}


class AuthorizationViewTestCase(TestCase):

    fixtures = [
        'weather_forecast_app/fixtures/db.json',
    ]

    def setUp(self) -> None:
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_create_user(self) -> None:
        self.client.logout()
        response = self.client.post(reverse(
            "authorization:register"),
            DATA,
        )
        queryset = User.objects.get(username=DATA["username"])
        self.assertEqual(queryset.username, DATA["username"])
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)

    def test_login_user(self) -> None:
        response = self.client.post(reverse(
            "authorization:login"),
            DATA,
        )
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertRedirects(response, reverse('forecast:city_form_view'))

    def test_logout_user(self) -> None:
        response = self.client.get(reverse(
            "authorization:logout"),
        )
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertRedirects(response, reverse('authorization:login'))
