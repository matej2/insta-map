import os

import django
from django.test import TestCase

# Create your tests here.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from photo.scraper import scrape_photos

scrape_photos()