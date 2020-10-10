import random
import re

from insta_map.proxy import get_using_proxy, proxy_generator
from location.models import Location
from photo.models import Photo

random.seed()


def scrape_photos():
    st = 0
    st2 = 0

    proxies = proxy_generator()

    # Caption remove
    reg = re.compile('\@\w+|\#\w+')
    # Caption block
    # TODO

    data = Location.objects.all()

    for d in data:
        pics = get_using_proxy(f'https://www.instagram.com/explore/locations/{d.id}/?__a=1', proxy=proxies)

        if pics is not False:
            pics_json = pics.json()["graphql"]["location"]

            location = d.name
            lat = pics_json["lat"]
            lng = pics_json["lng"]

            loc = Location.objects.get(id=d.id)
            loc.lat = lat
            loc.lng = lng
            loc.save()

            for r in pics_json['edge_location_to_media']['edges']:
                pic = r["node"]
                caption = ""

                if len(pic['edge_media_to_caption']['edges']) > 0:
                    caption = pic['edge_media_to_caption']['edges'][0]['node']['text']
                    caption = reg.sub("", caption)

                try:
                    p = Photo.objects.get(id=pic["id"])
                except Photo.DoesNotExist:
                    p = Photo()
                    p.id = pic["id"]
                p.thumbnail = pic["thumbnail_src"]
                p.caption = caption
                p.location = d
                p.save()

                # How many pictures for each location?
                st = st + 1
                if st > 2:
                    break

            print(f'Added photos for {location}')

            # How many locations to read?
            st2 = st2 + 1
            if st2 > 70:
                break
