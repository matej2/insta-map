# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from location.models import Location

class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "url", "website")

admin.site.register(Location, LocationAdmin)