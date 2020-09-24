import json

import requests as r

from insta_map.common import MyEncoder
from insta_map.settings import CITIES


def scrape_cities():
    res = r.get("https://www.instagram.com/explore/locations/SI/slovenia/?__a=1").json()
    cities = res["city_list"]

    with open(CITIES, "w") as file:
        file.write(json.dumps(cities, cls=MyEncoder))
