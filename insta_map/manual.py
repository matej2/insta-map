import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from city.scraper import CityScraper
from location.scraper import LocationScraper
from photo.scraper import PhotoScraper

CityScraper.scrape_cities()
LocationScraper.scrape_locations()
PhotoScraper.scrape_photos()