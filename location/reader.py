import json
import os
import random
from time import sleep

import requests as r

from insta_map.settings import BASE_DIR
from wall.test.tests import parse_location, parse_posts, MapData, create_test_json, City, Location

random.seed()


def get_json():
    dir = os.path.join(os.getcwd(), "test", "locations.json")
    url = f''
    c = 0
    arr = []

    with open(dir, "r") as file:  # Use file to refer to the file object
        data = file.read()
        obj = json.loads(data)
        l = obj["location_list"]

        for i in obj["location_list"]:

            res = r.get(f'https://www.instagram.com/explore/locations/{i["id"]}/ljubljana-slovenia/?__a=1').json()
            posts = parse_posts(res["graphql"])
            lat = res["graphql"]["location"]["lat"]
            lng = res["graphql"]["location"]["lng"]
            name = res["graphql"]["location"]["name"]
            loc = Location(i["id"], lat, lng, name)

            arr.append(MapData(loc, posts))

            print(res)
            if c >= 1:
                break
            c = c + 1
            sleep(random.random()*10)
    create_test_json(arr)

get_json()