import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from photo.scraper import PhotoScraper

PhotoScraper.get_photos()
