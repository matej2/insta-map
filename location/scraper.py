import random
import time
from json import JSONDecodeError

import requests

from city.models import City
from insta_map.common import get_proxy
from location.models import Location

random.seed()


def scrape_locations():
    res = []
    st = 0
    st2 = 0

    proxies = {
        'http': get_proxy()
    }
    print("started")

    data = City.objects.all()
    for d in data:

        try:
            loc = requests.get(f'https://www.instagram.com/explore/locations/{d.id}/?__a=1', proxies=proxies).json()


            for r in loc["location_list"]:

                if len(Location.objects.get(id=r["id"])) > 0:
                    l = Location.objects.get(id=r["id"])
                else:
                    l = Location.objects.create(id=r["id"], city_id=d.id)
                l.name=r["name"]
                l.save()

                st = st + 1

                print("Added location: {}".format(r["name"]))

                # How many locations for each city?
                if st > 2:
                    break

            # How many cities to read?
            st2 = st2 + 1
            if st2 > 50:
                break
        except KeyError:
            print("KeyError")
            continue
        except JSONDecodeError:
            print(f'Error decoding json. Skipping {d.id}')

        time.sleep((random.random() * 500) / 1000)
        print(f'Added {len(res)} locations for {d.name}')