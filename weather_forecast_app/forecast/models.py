# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = "name",

    name = models.CharField(max_length=50, blank=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    user_id = models.ManyToManyField(User)
