from rest_framework import serializers

from .models import City


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "id", "name", "latitude", "longitude", "count",
