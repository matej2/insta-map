from django.db import models

# Create your models here.
from location.models import Location


class Photo(models.Model):
    thumbnail = models.CharField(max_length=255, null=True)
    caption = models.CharField(max_length=255, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)