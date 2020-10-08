from city.models import City
from insta_map.proxy import get_using_proxy


def scrape_cities():
    res = get_using_proxy("https://www.instagram.com/explore/locations/SI/slovenia/?__a=1").json()
    cities = res["city_list"]

    for city in cities:
        c = City(name=city["name"])
        c.save()
