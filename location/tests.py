# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import django
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

# Create your tests here.
from location.scraper import scrape_locations

scrape_locations()