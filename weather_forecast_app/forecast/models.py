from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"
        ordering = "name",

    name = models.CharField(max_length=50, blank=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    count = models.IntegerField(default=0)
    user_id = models.ManyToManyField(User)

    def to_json(self):
        return {
            "id":self.id,
            "name": self.name,
            "latitude":self.latitude,
            "longitude": self.longitude
        }
