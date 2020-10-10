import random
import time
from json import JSONDecodeError

from city.models import City
from insta_map.proxy import get_using_proxy, proxy_generator
from location.models import Location

random.seed()


def scrape_locations():
    st = 0
    st2 = 0

    proxies = proxy_generator()

    data = City.objects.all()
    for d in data:

        try:
            loc = get_using_proxy(f'https://www.instagram.com/explore/locations/{d.id}/?__a=1', proxy=proxies,
                                  disable_proxy=True)

            if loc is not False:
                loc_json = loc.json()

                for r in loc_json["location_list"]:

                    try:
                        l = Location.objects.get(id=r["id"])
                    except Location.DoesNotExist:
                        l = Location()
                        l.id = r["id"]
                    l.city = d
                    l.name = r["name"]
                    l.url = 'https://www.instagram.com/explore/locations/' + d.id
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
            proxies = None
            print(f'Error decoding json. Skipping {d.id}. Invalidating proxy')

        time.sleep((random.random() * 500) / 1000)
