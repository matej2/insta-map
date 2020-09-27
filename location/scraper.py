import json
import random
import time
from json import JSONDecodeError

import requests

from insta_map.common import MyEncoder, get_proxy
from insta_map.settings import CITIES, LOCATIONS
from location.models import Location

random.seed()


def scrape_locations():
    res = []
    st = 0
    st2 = 0

    proxies = {
        'http': get_proxy()
    }

    with open(CITIES, "r") as file:
        data = json.loads(file.read())
        for d in data:

            try:
                loc = requests.get(f'https://www.instagram.com/explore/locations/{d["id"]}/?__a=1', proxies=proxies).json()


                for r in loc["location_list"]:
                    res.append(Location(r["id"], r["name"]))
                    st = st + 1

                    # How many locations for each city?
                    if st > 2:
                        break

                # How many cities to read?
                st2 = st2 + 1
                if st2 > 50:
                    break
            except KeyError:
                continue
            except JSONDecodeError:
                print(f'Error decoding json. Skipping {d["id"]}')

            time.sleep((random.random() * 500) / 1000)
            print(f'Added {len(res)} locations for {d["name"]}')

    with open(LOCATIONS, "w") as file:
        file.write(json.dumps(res, cls=MyEncoder))
