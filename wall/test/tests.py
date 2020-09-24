import json
import os
import pathlib

from insta_map.common import MyEncoder
from insta_map.settings import BASE_DIR


class City:
    def __init__(self, id, data):
        self.id = id
        self.data = data

class TestData:
    def __init__(self, thumbnail, caption):
        self.thumbnail = thumbnail
        self.caption = caption


class MapData:
    def __init__(self, meta, list):
        self.meta = meta
        self.list = list

def parse_location(obj):
    return Location(obj['location']['lat'], obj['location']['lng'], obj['location']['name'])

def parse_posts(obj):
    posts = obj['location']['edge_location_to_media']['edges']
    r = []

    for p in posts:
        if len(p['node']['edge_media_to_caption']['edges']) > 0:
            d = TestData(p['node']['thumbnail_src'], p['node']['edge_media_to_caption']['edges'][0]['node']['text'])
        else:
            d = TestData(p['node']['thumbnail_src'], "")
        r.append(d)
    return r

def read_posts():
    path = os.path.join(pathlib.Path(__file__).parent.absolute(), "wall-izola.json")

    with open(path, "r") as file:
        data = file.read()
        obj = json.loads(data)

        l = parse_location(obj)
        posts = parse_posts(obj)

    return MapData(l, posts)


def create_test_json(data):
    if data is None:
        data = read_posts()
    path = os.path.join(BASE_DIR, 'static', 'wall-izola_test.json')
    with open(path, "w") as file:
        file.write(json.dumps(data, cls=MyEncoder))


#create_test_json()
