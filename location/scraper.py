import json
import os
import random
import time
from json import JSONDecodeError

import requests

from city.models import City
from insta_map.proxy import get_json, proxy_generator
from location.models import Location

random.seed()
CITY_LIMIT = int(os.environ.get('CITY_LIMIT')) if os.environ.get('CITY_LIMIT') else 30
LOCATION_LIMIT = int(os.environ.get('LOCATION_LIMIT')) if os.environ.get('LOCATION_LIMIT') else 10

class LocationScraper():
    def scrape_locations(self):
        st = 0
        st2 = 0

        proxies = proxy_generator()

        data = City.objects.all()
        for d in data:

            try:
                loc = get_json(f'https://www.instagram.com/explore/locations/{d.id}/?__a=1', proxy=proxies,
                               disable_proxy=True)
                if loc is not False:
                    for r in loc["location_list"]:

                        try:
                            l = Location.objects.get(id=r["id"])
                        except Location.DoesNotExist:
                            l = Location()
                            l.id = r["id"]
                        l.city = d
                        l.name = r["name"][:254]
                        l.url = 'https://www.instagram.com/explore/locations/' + r["id"]
                        l.save()

                        st = st + 1

                        print("Added location: {}".format(r["name"]))

                        # How many locations for each city?
                        if st >= LOCATION_LIMIT:
                            break

                    # How many cities to read?
                    st2 = st2 + 1
                    if st2 >= CITY_LIMIT:
                        break
            except KeyError:
                print("KeyError")
                continue
            except JSONDecodeError:
                proxies = None
                print(f'Error decoding json. Skipping {d.id}. Invalidating proxy')

            time.sleep((random.random() * 500) / 1000)

    def process_locations(self, loc):
        try:
            l = Location.objects.get(loc['pk'])
        except (Location.DoesNotExist, TypeError):
            l = Location()
            l.id = loc['pk']
        l.name = loc['name'][:254]
        l.url = 'https://www.instagram.com/explore/locations/' + str(loc['pk'])
        l.save()

        return loc['pk']