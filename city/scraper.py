from city.models import City
from insta_map.proxy import get_using_proxy


def scrape_cities():
    res = get_using_proxy("https://www.instagram.com/explore/locations/SI/slovenia/?__a=1")
    if res is not False:
        res_json = res.json()
        cities = res_json["city_list"]

        for city in cities:
            try:
                c = City.objects.get(id=city["id"])
            except City.DoesNotExist:
                c = City.objects.create(id=city["id"], name=city["name"])
            c.save()
    else:
        print("No cities")
