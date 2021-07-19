import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from city.scraper import scrape_cities
from location.scraper import scrape_locations
from photo.scraper import scrape_photos

#scrape_cities(disable_proxy=True)
#scrape_locations()
scrape_photos()