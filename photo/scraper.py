import json
import random
import re
import time

import requests

from insta_map.common import MyEncoder, get_proxy
from insta_map.settings import PHOTOS, LOCATIONS, CITIES
from location.models import Location
from photo.models import PhotoData, PhotoMeta, Photo

random.seed()


def scrape_photos():
    res = []
    st = 0
    st2 = 0


    proxies = {
        'http': get_proxy()
    }


    # Caption remove
    p = re.compile('\@\w+|\#\w+')
    # Caption block
    # TODO

    data = Location.objects.all()

    for d in data:
        pics = requests.get(f'https://www.instagram.com/explore/locations/{d["id"]}/?__a=1', proxies=proxies).json()["graphql"][
            "location"]

        location = d["name"]
        lat = pics["lat"]
        lng = pics["lng"]

        loc = Location()



        photo_meta = PhotoMeta(location, lat, lng)
        photo_list = []

        for r in pics['edge_location_to_media']['edges']:
            pic = r["node"]
            caption = ""

            if len(pic['edge_media_to_caption']['edges']) > 0:
                caption = pic['edge_media_to_caption']['edges'][0]['node']['text']
                caption = p.sub("", caption)

            p = Photo()
            p.thumbnail = pic["thumbnail_src"]
            p.caption = caption
            p.location = d
            p.save()


            # Sleep for x milliseconds
            time.sleep((random.random() * 500) / 1000)

            # How many pictures for each location?
            st = st + 1
            if st > 2:
                break

        print(f'Added {len(photo_list)} photos for {location}')

        # How many locations to read?
        st2 = st2 + 1
        if st2 > 70:
            break

    with open(PHOTOS, "w") as file:
        file.write(json.dumps(res, cls=MyEncoder))
