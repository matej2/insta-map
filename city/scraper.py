from city.models import City
from insta_map.proxy import get_json


def scrape_cities():
    res = get_json("https://www.instagram.com/explore/locations/SI/slovenia/?__a=1")

    if res is not False:
        for city in res["city_list"]:
            try:
                c = City.objects.get(id=city["id"])
            except City.DoesNotExist:
                c = City.objects.create(id=city["id"], name=city["name"][:254])
            c.save()
