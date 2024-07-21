from .models import City
from rest_framework import serializers


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "name", "latitude", "longitude"
