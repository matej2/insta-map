import json
import random
import re
import time

import requests

from insta_map.proxy import proxy_generator

random.seed()

USERNAME = "matej.821"

def scrape_user_photos():
    res = []
    st = 0
    st2 = 0


    proxies = proxy_generator()


    # Caption remove
    p = re.compile('\@\w+|\#\w+')
    # Caption block
    # TODO


    user = requests.get(f'https://www.instagram.com/{USERNAME}/?__a=1', proxies=proxies).json()["graphql"][
        "user"]
    username = user["username"]

    for r in user['edge_owner_to_timeline_media']['edges']:
        pic = r["node"]
        caption = ""

        location_id = pic["location"]["id"]

        location = requests.get(f'https://www.instagram.com/explore/locations/{location_id}//?__a=1', proxies=proxies).json()["graphql"][
            "location"]

        location_name = location["name"]
        lat = location["lat"]
        lng = location["lng"]
        user_meta = UserMeta(location_name, lat, lng, username)

        if len(pic['edge_media_to_caption']['edges']) > 0:
            caption = pic['edge_media_to_caption']['edges'][0]['node']['text']
            caption = p.sub("", caption)


        # Sleep for x milliseconds
        time.sleep((random.random() * 500) / 1000)

        # How many pictures for each location?
        if st > 10:
            break

        if lat is not None or lng is not None:
            st = st + 1
            print(f'Added one photo for {user["username"]}')
            res.append(PhotoData(user_meta, [Photo(pic["thumbnail_src"], caption)]))


    with open(PHOTOS, "w") as file:
        file.write(json.dumps(res, cls=MyEncoder))
