import json
import os
import requests as r

from insta_map.settings import BASE_DIR


def get_json():
    dir = os.path.join(__file__, "test", "locations.json")
    url = f''
    with open(dir, "r") as file:  # Use file to refer to the file object
        data = file.read()
        obj = json.loads(data)
        r.get()
