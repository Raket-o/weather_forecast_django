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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from forecast.views import CityCountList

routers = DefaultRouter()
routers.register("forecast", CityCountList, basename='city_count_list')

urlpatterns = [
    path('', include('authorization.urls')),
    path('admin/', admin.site.urls),
    path("api/", include(routers.urls)),
    path('forecast/', include('forecast.urls')),
]

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
