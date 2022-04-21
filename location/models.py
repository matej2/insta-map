# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from city.models import City


class Location(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255, null=True, default="")
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    url = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str('{}:{}'.format(self.id, self.name))
