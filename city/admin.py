from django.contrib import admin

# Register your models here.
from city.models import City


class CityAdmin(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(City, CityAdmin)