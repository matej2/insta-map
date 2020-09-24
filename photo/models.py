from django.db import models

# Create your models here.

class PhotoMeta:
    def __init__(self, location, lat, lng):
        self.location = location
        self.lat = lat
        self.lng = lng

class PhotoData:
    def __init__(self, meta, list):
        self.meta = meta
        self.list = list

class Photo:
    def __init__(self, thumbnail, caption):
        self.thumbnail = thumbnail
        self.caption = caption