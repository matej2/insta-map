import os

import django
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

# Create your tests here.
from city.scraper import scrape_cities

scrape_cities()
