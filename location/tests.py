# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import unittest
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

from location.scraper import LocationScraper
from location.models import Location

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

# Create your tests here.

RESPONSE_LOCATION = json.loads('{ "address": "Ghitorni", "city": "New Delhi", "external_source": "facebook_places", "facebook_places_id": 351681088339814, "lat": 28.4969425, "lng": 77.1314828, "name": "Silver Oak Farms Ghithorni", "pk": 593593213, "short_name": "Silver Oak Farms Ghithorni" }')

class LocationScraperTest(unittest.TestCase):
    def test_process_locations(self):
        scraper = LocationScraper()
        loc_id = scraper.process_location(RESPONSE_LOCATION)

        self.assertIsNotNone(loc_id)

        Location.objects.filter(id=loc_id).delete()

