# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        # ordering = "count", "name"
        ordering = "name",

    name = models.CharField(max_length=50, blank=False)
    # count = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    user = models.ManyToManyField(User)
