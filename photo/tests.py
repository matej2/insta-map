import os

import django

# Create your tests here.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from photo.scraper import scrape_photos

scrape_photos()