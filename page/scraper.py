import os
import random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "insta_map.settings")
django.setup()

random.seed()

USERNAME = "matej.821"


def scrape_user_photos():
    return True
