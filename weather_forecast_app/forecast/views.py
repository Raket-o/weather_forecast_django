from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from .models import City
from .forms import CityForm
from django.urls import reverse_lazy

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .utils import get_forecat_weather, get_geo_location_by_name_city


def cities_list_view(request, cities_list: list) -> HttpResponseRedirect:
    # cities_list = get_geo_location_by_name_city("Samara")
    # print(cities_list)
    # cities_list = {'results': [
    #     {'id': 499099, 'name': 'Самара', 'latitude': 53.20007, 'longitude': 50.15, 'elevation': 117.0,
    #      'feature_code': 'PPLA', 'country_code': 'RU', 'admin1_id': 499068, 'timezone': 'Europe/Samara',
    #      'population': 1134730, 'country_id': 2017370, 'country': 'Россия', 'admin1': 'Самарская область'},
    #     {'id': 91597, 'name': 'Sāmarrā’', 'latitude': 34.1959, 'longitude': 43.88568, 'elevation': 80.0,
    #      'feature_code': 'PPLA2', 'country_code': 'IQ', 'admin1_id': 91695, 'admin2_id': 6783103,
    #      'timezone': 'Asia/Baghdad', 'population': 158508, 'country_id': 99237, 'country': 'Ирак',
    #      'admin1': 'Muhafazat Salah ad Din', 'admin2': 'Al-Daur District'},
    #     {'id': 3621990, 'name': 'Sámara', 'latitude': 9.88147, 'longitude': -85.52809, 'elevation': 10.0,
    #      'feature_code': 'PPL', 'country_code': 'CR', 'admin1_id': 3623582, 'admin2_id': 3622715, 'admin3_id': 11239401,
    #      'timezone': 'America/Costa_Rica', 'population': 1071, 'country_id': 3624060, 'country': 'Коста-Рика',
    #      'admin1': 'Provincia de Guanacaste', 'admin2': 'Nicoya', 'admin3': 'Sámara'},
    #     {'id': 668121, 'name': 'Sămara', 'latitude': 44.82574, 'longitude': 24.71409, 'elevation': 315.0,
    #      'feature_code': 'PPL', 'country_code': 'RO', 'admin1_id': 686192, 'admin2_id': 670074,
    #      'timezone': 'Europe/Bucharest', 'population': 571, 'country_id': 798549, 'country': 'Румыния',
    #      'admin1': 'Argeş', 'admin2': 'Comuna Poiana Lacului'},
    #     {'id': 499097, 'name': 'Самара', 'latitude': 59.96944, 'longitude': 34.38556, 'elevation': 119.0,
    #      'feature_code': 'PPL', 'country_code': 'RU', 'admin1_id': 536199, 'timezone': 'Europe/Moscow',
    #      'country_id': 2017370, 'country': 'Россия', 'admin1': 'Ленинградская область'},
    #     {'id': 499098, 'name': 'Самара', 'latitude': 54.01264, 'longitude': 38.83453, 'elevation': 166.0,
    #      'feature_code': 'PPL', 'country_code': 'RU', 'admin1_id': 500059, 'timezone': 'Europe/Moscow',
    #      'country_id': 2017370, 'country': 'Россия', 'admin1': 'Рязанская область'},
    #     {'id': 499100, 'name': 'Самара', 'latitude': 52.3573, 'longitude': 34.998, 'elevation': 225.0,
    #      'feature_code': 'PPL', 'country_code': 'RU', 'admin1_id': 514801, 'timezone': 'Europe/Moscow',
    #      'country_id': 2017370, 'country': 'Россия', 'admin1': 'Орловская область'},
    #     {'id': 806710, 'name': 'Samara', 'latitude': 50.98083, 'longitude': 34.39605, 'elevation': 146.0,
    #      'feature_code': 'PPL', 'country_code': 'UA', 'admin1_id': 692196, 'timezone': 'Europe/Kiev',
    #      'country_id': 690791, 'country': 'Украина', 'admin1': 'Сумская область'},
    #     {'id': 1027559, 'name': 'Samara', 'latitude': -11.87667, 'longitude': 34.93806, 'elevation': 570.0,
    #      'feature_code': 'PPL', 'country_code': 'MZ', 'timezone': 'Africa/Maputo', 'country_id': 1036973,
    #      'country': 'Мозамбик'},
    #     {'id': 1493153, 'name': 'Самара', 'latitude': 54.91667, 'longitude': 60.91667, 'elevation': 270.0,
    #      'feature_code': 'PPL', 'country_code': 'RU', 'admin1_id': 1508290, 'timezone': 'Asia/Yekaterinburg',
    #      'country_id': 2017370, 'country': 'Россия', 'admin1': 'Челябинская'}], 'generationtime_ms': 1.0809898}
    # cities_list = cities_list.get('results')
    return render(request, template_name="forecast/cities_list.html", context={"cities_list": cities_list})


def request_city_from_user(request):
    # cities_list = get_geo_location_by_name_city("Samara")
    # print(cities_list)
    if request.method == 'GET':
        form = CityForm()
        # form = CityForm(request.GET)
        if form.is_valid():
            ciy_name = form.cleaned_data['name']

        # counter_amount = get_conversion_amount(base_currency, counter_currency, datetime.now(), base_amount)
        response = HttpResponseRedirect('/')
        context = {'city': form}

        return render(request, template_name='../templates/forecast/cities_list.html', context=context)

        # response['base_currency'] = base_currency
        # response['counter_currency'] = counter_currency
        # response['base_amount'] = base_amount
        # return response

    else:
        form = CityForm()
        context = {'city': form}
        print(context)

        return render(request, template_name='../templates/forecast/cities_list.html', context=context)

# class CitiesListView(ListView):
#     template_name = "forecast/cities_list.html"
#     queryset = (
#         City.objects
#         .all()
#     )


# class CityCreateView(CreateView):
#     model = City
#     form_class = CityForm
#     success_url = reverse_lazy("forecast:cities_list_view")
#
#     def form_valid(self, form) -> None:
#         city = form.cleaned_data.get("name")
#         print("CityCreateView", city)
#         from .utils import get_geo_location_by_name_city
#         result = get_geo_location_by_name_city(city)
#         print(result)
#         # form.instance.created_by = self.request.user
#         response = super().form_valid(form)
#         return response
