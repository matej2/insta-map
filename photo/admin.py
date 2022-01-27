from django.contrib import admin

# Register your models here.
from photo.models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "thumbnail", "accessibility_caption", "url")

admin.site.register(Photo, PhotoAdmin)