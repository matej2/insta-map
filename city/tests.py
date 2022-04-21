import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

# Create your tests here.
from city.scraper import scrape_cities

scrape_cities()
