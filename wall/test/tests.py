import json
import os
from json import JSONEncoder
from insta_map.settings import BASE_DIR


class Location:
    def __init__(self, lat, lng, name):
        self.lat = lat
        self.lng = lng
        self.name = name


class TestData:
    def __init__(self, thumbnail, caption):
        self.thumbnail = thumbnail
        self.caption = caption


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class MapData:
    def __init__(self, meta, list):
        self.meta = meta
        self.list = list


def read_posts():
    response = []
    with open("wall-izola.json", "r") as file:  # Use file to refer to the file object
        data = file.read()
        obj = json.loads(data)

        l = Location(obj['graphql']['location']['lat'],obj['graphql']['location']['lng'], obj['graphql']['location']['name'])
        posts = obj['graphql']['location']['edge_location_to_media']['edges']

        for p in posts:
            if len(p['node']['edge_media_to_caption']['edges']) > 0:
                d = TestData(p['node']['thumbnail_src'], p['node']['edge_media_to_caption']['edges'][0]['node']['text'])
            else:
                d = TestData(p['node']['thumbnail_src'], "")
            response.append(d)

    return MapData(l, response  )


def create_test_json():
    data = read_posts()
    path = os.path.join(BASE_DIR, 'static', 'wall-izola_test.json')
    with open(path, "w") as file:
        file.write(json.dumps(data, cls=MyEncoder))


create_test_json()
