"""
URL configuration for weather_forecast_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import DefaultRouter

from forecast.models import City
from forecast.serializers import CitySerializers
from rest_framework.generics import ListAPIView

# from django.db.models import Count
#
# sql_query = """
# SELECT forecast_city.name, forecast_city.latitude, forecast_city.longitude, count(*) as count
# FROM forecast_city
# GROUP BY forecast_city.name, forecast_city.latitude, forecast_city.longitude
# ORDER BY count DESC, forecast_city.name;
#         """
# with connection.cursor() as cursor:
#     cursor.execute(sql_query)
#     results = cursor.fetchall()

from forecast.views import CityCountList


routers = DefaultRouter()
routers.register("forecast", CityCountList, basename='city_count_list')

urlpatterns = [
    path('', include('authorization.urls')),
    path('admin/', admin.site.urls),
    path("api/", include(routers.urls)),
    path('forecast/', include('forecast.urls')),

    # path('auth/', include('authorization.urls')),
    # path('accounts/', include('authorization.urls')),
    # path('statistics/', include('customer_statistics.urls')),
    # path('services/', include('services.urls')),
    # path('advertising-companies/', include('advertising_companies.urls')),
    # path('clients/', include('clients.urls')),
    # path('contracts/', include('contracts.urls')),
    #
    # path("api/", include(routers.urls)),
    # path('api/', include('djoser.urls.authtoken')),

    # path(
    #     'api/cities',
    #     ListAPIView.as_view(
    #         # queryset=City.objects.all(),
    #         # queryset=City.objects.all().values("name", "latitude", "longitude").annotate(count=Count(["name", "latitude", "longitude",], distinct=True)).order_by(),
    #         queryset=City.objects.all().values("name", "latitude", "longitude").
    #             annotate(count=Count("id", distinct=True)).order_by("-"),
    #         serializer_class=CitySerializers
    #     ),
    #     name='count_cities'
    # )
]

# cities_list = (City.objects.filter(user_id=self.request.user.pk).
#                values("name", "latitude", "longitude").distinct().
#                order_by("name"))
# count = Project.objects.values('informationunit__username').distinct().count()
# cities_list = (City.objects.filter(user_id=self.request.user.pk).
#                values("name", "latitude", "longitude").distinct().
#                order_by("name"))


if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )

    urlpatterns.append(
        path('__debug__/', include('debug_toolbar.urls')),
    )

    urlpatterns += staticfiles_urlpatterns()