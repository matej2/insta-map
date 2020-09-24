import json
import random
import time

import requests

from insta_map.common import MyEncoder
from insta_map.settings import CITIES, LOCATIONS
from location.models import Location

random.seed()


def scrape_locations():
    res = []
    st = 0
    st2 = 0

    with open(CITIES, "r") as file:
        data = json.loads(file.read())
        for d in data:
            loc = requests.get(f'https://www.instagram.com/explore/locations/{d["id"]}/?__a=1').json()

            for r in loc["location_list"]:
                res.append(Location(r["id"], r["name"]))
                st = st + 1

                if st > 10:
                    break

            st2 = st2 + 1
            if st2 > 10:
                break

        time.sleep((random.random() * 500) / 1000)


    with open(LOCATIONS, "w") as file:
        file.write(json.dumps(res, cls=MyEncoder))
